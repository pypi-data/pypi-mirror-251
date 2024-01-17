from __future__ import annotations

from typing import Literal

import torch
from graph_pes.core import GraphPESModel
from graph_pes.data.atomic_graph import AtomicGraph
from graph_pes.nn import MLP, PerSpeciesEmbedding, ShiftedSoftplus
from torch import nn
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import scatter

from .distances import (
    Bessel,
    DistanceExpansion,
    GaussianSmearing,
    PolynomialEnvelope,
)


class CFConv(MessagePassing):
    r"""
    CFConv: The Continous Filter Convolution

    Originally proposed as part of `SchNet <https://arxiv.org/abs/1706.08566>`_,
    this message passing layer creates messages of the form:

    .. math::
        m_{ij} = x_j \odot \mathbb{F}(r_{ij})

    where :math:`\mathbb{F}` is some learnable filter function which
    expands the radial distance :math:`r_{ij}` into a set of features
    that match the dimensionality of the node features :math:`x_j`.

    Parameters
    ----------
    filter_generator : nn.Module
        The filter function :math:`\mathbb{F}`.
    """

    def __init__(self, filter_generator: nn.Module):
        super().__init__(aggr="add")
        self.filter_generator = filter_generator

    def message(
        self, x_j: torch.Tensor, neighbour_distances: torch.Tensor
    ) -> torch.Tensor:
        """
        Apply the filter function to the distances and multiply by the
        node features.

        Parameters
        ----------
        x_j : torch.Tensor
            The node features of the neighbors.
        neighbour_distances : torch.Tensor
            The distances to the neighbors.
        """
        filters = self.filter_generator(neighbour_distances)
        return x_j * filters

    def forward(
        self,
        neighbour_index: torch.Tensor,
        neighbour_distances: torch.Tensor,
        node_features: torch.Tensor,
    ) -> torch.Tensor:
        return self.propagate(
            neighbour_index,
            neighbour_distances=neighbour_distances,
            x=node_features,
        )

    def __repr__(self):
        rep = f"CFConv({self.filter_generator})"
        if len(rep) > 40:
            indented = "  " + "\n  ".join(
                str(self.filter_generator).split("\n")
            )
            rep = f"CFConv(\n{indented}\n)"
        return rep


class SchNetInteraction(nn.Module):
    r"""
    SchNet interaction block.

    Updates the embedding of each atom, :math:`x_i` by sequentially
    applying the following:
    - a linear transform of each node's features :math:`h_i \leftarrow W x_i`
    - a message passing cfconv block that replaces the current node's features
        with a sum over the distance-filtered features of its neighbors
        :math:`h_i \leftarrow \sum_{j \in \mathcal{N}(i)}
        \mathbb{F}(r_{ij}) \odot h_j`
    - a multilayer perceptron that further embeds these new node features
        :math:`h_i \leftarrow \mathrm{MLP}(h_i)`

    Parameters
    ----------
    n_features : int
        Number of features per node.
    expansion_features : int
        Number of features used for the radial basis expansion.
    cutoff : float
        Neighborhood cutoff radius.
    """

    def __init__(
        self,
        n_features: int,
        expansion_features: int,
        cutoff: float,
        basis_type: type[DistanceExpansion] = GaussianSmearing,
    ):
        super().__init__()

        # schnet interaction block's are composed of 3 elements

        # 1. linear transform to get new node features
        self.linear = nn.Linear(n_features, n_features)

        # 2. cfconv to mix these new features with distances information,
        # and aggregate over neighbors to create completely new node features
        filter_generator = nn.Sequential(
            basis_type(expansion_features, cutoff),
            MLP(
                [expansion_features, n_features, n_features],
                activation=ShiftedSoftplus(),
            ),
        )
        self.cfconv = CFConv(filter_generator)

        # 3. mlp to further embed these new node features
        self.mlp = MLP(
            [n_features, n_features, n_features],
            activation=ShiftedSoftplus(),
        )

    def forward(
        self,
        neighbour_index: torch.Tensor,
        neighbour_distances: torch.Tensor,
        node_features: torch.Tensor,
    ):
        # 1. linear transform to get new node features
        h = self.linear(node_features)
        # 2. cfconv to mix these new features with distances information,
        # and aggregate over neighbors to create completely new node features
        h = self.cfconv(neighbour_index, neighbour_distances, h)
        # 3. mlp to further embed these new node features
        return self.mlp(h)


class SchNet(GraphPESModel):
    def __init__(
        self,
        node_feature_size: int,
        expansion_feature_size: int,
        cutoff: float,
        num_interactions: int = 3,
        basis_type: type[DistanceExpansion] = GaussianSmearing,
    ):
        super().__init__()

        self.chemical_embedding = PerSpeciesEmbedding(
            dim=node_feature_size, default=None
        )

        self.interactions = nn.ModuleList(
            SchNetInteraction(
                node_feature_size, expansion_feature_size, cutoff, basis_type
            )
            for _ in range(num_interactions)
        )

        self.read_out = MLP(
            [node_feature_size, node_feature_size // 2, 1],
            activation=ShiftedSoftplus(),
        )

    def predict_local_energies(self, graph: AtomicGraph) -> torch.Tensor:
        h = self.chemical_embedding(graph.Z)

        for interaction in self.interactions:
            h = h + interaction(
                graph.neighbour_index, graph.neighbour_distances, h
            )

        return self.read_out(h)


class ImprovedSchNetInteraction(nn.Module):
    def __init__(
        self,
        cutoff: float,
        radial_features: int = 8,
        radial_expansion: type[DistanceExpansion] = Bessel,
        atom_features: int = 4,
        mlp_height: int = 16,
        mlp_depth: int = 3,
        activation: type[nn.Module] = nn.CELU,
        pre_embed: bool = True,
    ):
        super().__init__()

        # radial filter components
        self.envelope = PolynomialEnvelope(cutoff)
        self.raw_filter_generator = nn.Sequential(
            radial_expansion(radial_features, cutoff),
            MLP(
                [radial_features, mlp_height, mlp_height, atom_features],
                activation=activation(),
            ),
        )

        # atom embedding components
        self.pre_embed = pre_embed
        if pre_embed:
            self.pre_embedding = MLP(
                [atom_features] + [mlp_height] * mlp_depth + [atom_features],
                activation=activation(),
            )
        self.post_embedding = MLP(
            [atom_features] + [mlp_height] * mlp_depth + [atom_features],
            activation=activation(),
        )

    def get_radial_embeddings(self, distances: torch.Tensor) -> torch.Tensor:
        envelope = self.envelope(distances).unsqueeze(-1)
        radial_embedding = self.raw_filter_generator(distances)
        return radial_embedding * envelope

    def forward(
        self,
        central_atom_embeddings: torch.Tensor,
        graph: AtomicGraph,
    ) -> torch.Tensor:
        # get radial features
        radial_embedding = self.get_radial_embeddings(graph.neighbour_distances)

        if self.pre_embed:
            # update atomic features
            central_atom_embeddings = self.pre_embedding(
                central_atom_embeddings
            )

        # haddamard product to mix atomic features with radial features
        i, j = graph.neighbour_index
        neighbour_atom_embeddings = central_atom_embeddings[j]
        messages = neighbour_atom_embeddings * radial_embedding

        # aggregate over neighbours to get new central atom embeddings
        central_atom_embeddings = scatter(messages, i, reduce="add")

        # update atomic features
        return self.post_embedding(central_atom_embeddings)


class ImprovedSchNet(GraphPESModel):
    def __init__(
        self,
        cutoff: float,
        radial_features: int = 8,
        radial_expansion: type[DistanceExpansion] = Bessel,
        atom_features: int = 4,
        mlp_height: int = 16,
        mlp_depth: int = 3,
        activation: type[nn.Module] = nn.CELU,
        num_blocks: int = 3,
        residual_messages: bool = True,
        pre_embed: Literal["none", "all", "2+"] = "2+",
    ):
        super().__init__()

        self.residual_messages = residual_messages

        self.chemical_embedding = PerSpeciesEmbedding(dim=atom_features)

        def _rule(i):
            return {
                "none": False,
                "all": True,
                "2+": i > 0,
            }[pre_embed]

        self.interactions = nn.ModuleList(
            ImprovedSchNetInteraction(
                cutoff,
                radial_features,
                radial_expansion,
                atom_features,
                mlp_height,
                mlp_depth,
                activation,
                pre_embed=_rule(i),
            )
            for i in range(num_blocks)
        )

        self.read_outs = nn.ModuleList(
            MLP(
                [atom_features] + [mlp_height] * mlp_depth + [1],
                activation=activation(),
            )
            for _ in range(num_blocks)
        )

    def predict_local_energies(self, graph: AtomicGraph) -> torch.Tensor:
        return self.per_block_predictions(graph).sum(dim=1)

    def per_block_predictions(self, graph: AtomicGraph) -> torch.Tensor:
        h = self.chemical_embedding(graph.Z)

        predictions = []
        for block, read_out in zip(self.interactions, self.read_outs):
            if self.residual_messages:
                h = block(h, graph) + h
            else:
                h = block(h, graph)
            predictions.append(read_out(h).squeeze())

        return torch.stack(predictions, dim=1)
