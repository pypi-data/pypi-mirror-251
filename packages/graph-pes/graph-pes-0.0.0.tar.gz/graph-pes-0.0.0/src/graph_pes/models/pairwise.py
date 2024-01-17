from __future__ import annotations

from abc import ABC, abstractmethod

import torch
from graph_pes.core import EnergySummation, GraphPESModel
from graph_pes.data import AtomicGraph
from graph_pes.data.batching import AtomicGraphBatch
from graph_pes.nn import PositiveParameter
from graph_pes.transform import PerAtomScale, PerAtomShift
from jaxtyping import Float
from torch import Tensor, nn

from .distances import Envelope


class PairPotential(GraphPESModel, ABC):
    r"""
    An abstract base class for PES models that calculate system energy as
    a sum over pairwise interactions:

    .. math::
        E = \sum_{i, j} V(r_{ij}, Z_i, Z_j)

    where :math:`r_{ij}` is the distance between atoms :math:`i` and :math:`j`,
    and :math:`Z_i` and :math:`Z_j` are their atomic numbers.
    This can be recast as a sum over local energy contributions,
    :math:`E = \sum_i \varepsilon_i`, according to:

    .. math::
        \varepsilon_i = \frac{1}{2} \sum_j V(r_{ij}, Z_i, Z_j)

    Subclasses should implement :meth:`interaction`.
    """

    @abstractmethod
    def interaction(
        self,
        r: Float[Tensor, "E"],
        Z_i: Float[Tensor, "E"],
        Z_j: Float[Tensor, "E"],
    ) -> Float[Tensor, "E"]:
        """
        Compute the interactions between pairs of atoms, given their
        distances and atomic numbers.

        Parameters
        ----------
        r
            The pair-wise distances between the atoms.
        Z_i
            The atomic numbers of the central atoms.
        Z_j
            The atomic numbers of the neighbours.

        Returns
        -------
        V: Float[Tensor, "E"]
            The pair-wise interactions.
        """

    def predict_local_energies(
        self, graph: AtomicGraph
    ) -> Float[Tensor, "graph.n_edges"]:
        central_atoms, neighbours = graph.neighbour_index
        distances = graph.neighbour_distances

        Z_i, Z_j = graph.Z[central_atoms], graph.Z[neighbours]
        V = self.interaction(
            distances.view(-1, 1), Z_i.view(-1, 1), Z_j.view(-1, 1)
        )

        # sum over the neighbours
        energies = torch.zeros_like(graph.Z, dtype=torch.float)
        energies.scatter_add_(0, central_atoms, V.squeeze())

        # divide by 2 to avoid double counting
        return energies / 2


class LennardJones(PairPotential):
    r"""
    A pair potential of the form:

    .. math::
        V(r_{ij}, Z_i, Z_j) = V(r_{ij}) = 4 \varepsilon \left[ \left(
        \frac{\sigma}{r_{ij}} \right)^{12} - \left( \frac{\sigma}{r_{ij}}
        \right)^{6} \right]

    where :math:`r_{ij}` is the distance between atoms :math:`i` and :math:`j`.
    Internally, :math:`\varepsilon` and :math:`\sigma` are stored as
    :class:`PositiveParameter <graph_pes.nn,PositiveParamerer>` instances,
    which ensures that they are kept strictly positive during training.

    Attributes
    ----------
    epsilon: :class:`PositiveParameter <graph_pes.nn.PositiveParameter>`
        The depth of the potential.
    sigma: :class:`PositiveParameter <graph_pes.nn.PositiveParameter>`
        The distance at which the potential is zero.
    """

    def __init__(self):
        super().__init__()
        self.epsilon = PositiveParameter(0.1)
        self.sigma = PositiveParameter(1.0)

        # epsilon is a scaling term, so only need to learn a shift
        # parameter (rather than a shift and scale)
        self._energy_summation = EnergySummation(local_transform=PerAtomShift())

    def interaction(
        self, r: torch.Tensor, Z_i: torch.Tensor, Z_j: torch.Tensor
    ):
        """
        Evaluate the pair potential.

        Parameters
        ----------
        r : torch.Tensor
            The pair-wise distances between the atoms.
        Z_i : torch.Tensor
            The atomic numbers of the central atoms. (unused)
        Z_j : torch.Tensor
            The atomic numbers of the neighbours. (unused)
        """
        x = self.sigma / r
        return 4 * self.epsilon * (x**12 - x**6)

    def pre_fit(self, graph: AtomicGraphBatch, energy_label: str = "energy"):
        super().pre_fit(graph, energy_label)

        # set the distance at which the potential is zero to be
        # close to the minimum pair-wise distance
        d = torch.quantile(graph.neighbour_distances, 0.01)
        self.sigma = PositiveParameter(d)


class Morse(PairPotential):
    r"""
    A pair potential of the form:

    .. math::
        V(r_{ij}, Z_i, Z_j) = V(r_{ij}) = D (1 - e^{-a(r_{ij} - r_0)})^2

    where :math:`r_{ij}` is the distance between atoms :math:`i` and :math:`j`,
    and :math:`D`, :math:`a` and :math:`r_0` control the depth, width and
    center of the potential well, respectively. Internally, these are stored
    as :class:`PositiveParameter` instances.

    Attributes
    ----------
    D: :class:`PositiveParameter <graph_pes.nn.PositiveParameter>`
        The depth of the potential.
    a: :class:`PositiveParameter <graph_pes.nn.PositiveParameter>`
        The width of the potential.
    r0: :class:`PositiveParameter <graph_pes.nn.PositiveParameter>`
        The center of the potential.
    """

    def __init__(self):
        super().__init__()
        self.D = PositiveParameter(0.1)
        self.a = PositiveParameter(1.0)
        self.r0 = PositiveParameter(0.5)

        # D is a scaling term, so only need to learn a shift
        # parameter (rather than a shift and scale)
        self._energy_summation = EnergySummation(local_transform=PerAtomScale())

    def interaction(
        self, r: torch.Tensor, Z_i: torch.Tensor, Z_j: torch.Tensor
    ):
        """
        Evaluate the pair potential.

        Parameters
        ----------
        r : torch.Tensor
            The pair-wise distances between the atoms.
        Z_i : torch.Tensor
            The atomic numbers of the central atoms. (unused)
        Z_j : torch.Tensor
            The atomic numbers of the neighbours. (unused)
        """
        return self.D * (1 - torch.exp(-self.a * (r - self.r0))) ** 2

    def pre_fit(self, graph: AtomicGraphBatch):
        super().pre_fit(graph)

        # set the potential depth to be shallow
        self.D = PositiveParameter(0.1)

        # set the center of the well to be close to the minimum pair-wise
        # distance
        d = torch.quantile(graph.neighbour_distances, 0.01)
        self.r0 = PositiveParameter(d)

        # set the width to be broad
        self.a = PositiveParameter(0.5)


class LearnablePairPotential(PairPotential):
    r"""
    A pair potential of the form:

    .. math::
        V(r_{ij}, Z_i, Z_j) = V(r_{ij}) = \text{Envelope}(r_{ij}) \circ
        f_\theta(r_{ij})

    where:

    * :math:`r_{ij}` is the distance between atoms :math:`i` and :math:`j`
    * :math:`f_\theta: \mathbb{R}^{\text{batch} \times 1} \rightarrow
      \mathbb{R}^{\text{batch} \times 1}, r \mapsto V(r)` is a learnable
      function parameterised by :math:`\theta`.
    * :math:`\text{Envelope} : \mathbb{R}^{\text{batch} \times 1} \rightarrow
      \mathbb{R}^{\text{batch} \times 1}` is an envelope function that ensures
      smoothness of the potential at the cutoff distance.

    Parameters
    ----------
    f
        The learnable element.
    envelope
        The envelope.
    """

    def __init__(self, f: nn.Module, envelope: Envelope):
        super().__init__()
        self.f = f
        self.envelope = envelope

    def interaction(
        self,
        r: Float[Tensor, "E 1"],
        Z_i: torch.Tensor | None = None,
        Z_j: torch.Tensor | None = None,
    ) -> Float[Tensor, "E 1"]:
        return self.f(r) * self.envelope(r)
