from __future__ import annotations

from abc import ABC, abstractmethod

import torch
from graph_pes.data import AtomicGraph
from graph_pes.data.batching import AtomicGraphBatch, sum_per_structure
from graph_pes.transform import (
    Chain,
    Identity,
    PerAtomScale,
    Transform,
)
from graph_pes.util import Keys, differentiate, require_grad
from jaxtyping import Float
from torch import Tensor, nn


class GraphPESModel(nn.Module, ABC):
    r"""
    An abstract base class for all graph-based, energy-conserving models of the
    PES that make predictions of the total energy of a structure as a sum
    of local contributions:

    .. math::
        E(\mathcal{G}) = \sum_i \varepsilon_i

    To create such a model, implement :meth:`predict_local_energies`,
    which takes an :class:`AtomicGraph`, or an :class:`AtomicGraphBatch`,
    and returns a per-atom prediction of the local energy. For a simple example,
    see :class:`LennardJones <graph_pes.models.pairwise.LennardJones>`.

    Under the hood, :class:`GraphPESModel` contains an
    :class:`EnergySummation` module, which is responsible for
    summing over local energies to obtain the total energy/ies,
    with optional transformations of the local and total energies.
    By default, this learns a per-species, local energy offset and scale.

    .. note::
        All :class:`GraphPESModel` instances are also instances of
        :class:`torch.nn.Module`. This allows for easy optimisation
        of parameters, and automated save/load functionality.
    """

    # TODO: fix this for the case of an isolated atom, either by itself
    # or within a batch: perhaps that should go in sum_per_structure?
    # or maybe default to a local scale followed by a global peratomshift?
    @abstractmethod
    def predict_local_energies(
        self, graph: AtomicGraph | AtomicGraphBatch
    ) -> Float[Tensor, "graph.n_atoms"]:
        """
        Predict the (standardized) local energy for each atom in the graph.

        Parameters
        ----------
        graph
            The graph representation of the structure/s.
        """

    def forward(self, graph: AtomicGraph | AtomicGraphBatch):
        """
        Predict the total energy of the structure/s.

        Parameters
        ----------
        graph : AtomicGraph
            The graph representation of the structure/s.
        """

        # local predictions
        local_energies = self.predict_local_energies(graph).squeeze()

        # sum over atoms to get total energy
        return self._energy_summation(local_energies, graph)

    def __init__(self):
        super().__init__()
        self._energy_summation = EnergySummation()

    def __repr__(self):
        # modified from torch.nn.Module.__repr__
        # changes:
        # - don't print any modules that start with _

        # We treat the extra repr like the sub-module, one item per line
        extra_lines = []
        extra_repr = self.extra_repr()
        # empty string will be split into list ['']
        if extra_repr:
            extra_lines = extra_repr.split("\n")
        child_lines = []
        for key, module in self._modules.items():
            if key.startswith("_"):
                continue
            mod_str = repr(module)
            mod_str = nn.modules.module._addindent(mod_str, 2)
            child_lines.append("(" + key + "): " + mod_str)
        lines = extra_lines + child_lines

        main_str = self._get_name() + "("
        if lines:
            # simple one-liner info, which most builtin Modules will use
            if len(extra_lines) == 1 and not child_lines:
                main_str += extra_lines[0]
            else:
                main_str += "\n  " + "\n  ".join(lines) + "\n"

        main_str += ")"
        return main_str

    def __add__(self, other: GraphPESModel) -> Ensemble:
        """
        A convenient way to create a summation of two models.

        Examples
        --------
        >>> TwoBody() + ThreeBody()
        Ensemble([TwoBody(), ThreeBody()], aggregation=sum)
        """

        return Ensemble([self, other], mean=False)

    def pre_fit(self, graphs: AtomicGraphBatch, energy_label: str = "energy"):
        """
        Perform optional pre-processing of the training data.

        By default, this fits a :class:`graph_pes.transform.PerAtomShift`
        and :class:`graph_pes.transform.PerAtomScale` to the energies
        of the training data, such that, before training, a unit-Normal
        output by the underlying model will result in energy predictions
        that are distributed according to the training data.

        Parameters
        ----------
        graphs
            The training data.
        """
        self._energy_summation.fit_to_graphs(graphs, energy_label)


class EnergySummation(nn.Module):
    def __init__(
        self,
        local_transform: Transform | None = None,
        total_transform: Transform | None = None,
    ):
        super().__init__()

        # if both None, default to a per-species, local energy offset
        if local_transform is None and total_transform is None:
            local_transform = Chain(
                [PerAtomScale(), PerAtomScale()], trainable=True
            )
        self.local_transform: Transform = local_transform or Identity()
        self.total_transform: Transform = total_transform or Identity()

    def forward(self, local_energies: torch.Tensor, graph: AtomicGraphBatch):
        local_energies = self.local_transform.inverse(local_energies, graph)
        total_E = sum_per_structure(local_energies, graph)
        total_E = self.total_transform.inverse(total_E, graph)
        return total_E

    def fit_to_graphs(
        self,
        graphs: AtomicGraphBatch | list[AtomicGraph],
        energy_label: str = "energy",
    ):
        if not isinstance(graphs, AtomicGraphBatch):
            graphs = AtomicGraphBatch.from_graphs(graphs)

        for transform in [self.local_transform, self.total_transform]:
            transform.fit(graphs[energy_label], graphs)


class Ensemble(GraphPESModel):
    def __init__(self, models: list[GraphPESModel], mean: bool = True):
        super().__init__()
        self.models: list[GraphPESModel] = nn.ModuleList(models)  # type: ignore
        self.mean = mean

    def predict_local_energies(self, graph: AtomicGraph | AtomicGraphBatch):
        s = sum(m.predict_local_energies(graph).squeeze() for m in self.models)
        return s / len(self.models) if self.mean else s

    def __repr__(self):
        aggregation = "mean" if self.mean else "sum"
        return f"Ensemble({self.models}, aggregation={aggregation})"


# TODO: add training flag to this so that we don't create the graph needlessly
# when in eval mode
def get_predictions(
    pes: GraphPESModel,
    structure: AtomicGraph | AtomicGraphBatch | list[AtomicGraph],
    property_labels: dict[Keys, str] | None = None,
) -> dict[str, torch.Tensor]:
    """
    Evaluate the `pes` on `structure` to get the labels requested.

    Parameters
    ----------
    pes
        The PES to use.
    structure
        The atomic structure to evaluate.
    property_labels
        The names of the properties to return. If None, all available
        properties are returned.

    Returns
    -------
    dict[str, torch.Tensor]
        The requested properties.

    Examples
    --------
    >>> # TODO

    """

    if isinstance(structure, list):
        structure = AtomicGraphBatch.from_graphs(structure)

    if property_labels is None:
        property_labels = {
            Keys.ENERGY: "energy",
            Keys.FORCES: "forces",
        }
        if structure.has_cell:
            property_labels[Keys.STRESS] = "stress"

    else:
        if Keys.STRESS in property_labels and not structure.has_cell:
            raise ValueError("Can't predict stress without cell information.")

    predictions = {}

    # setup for calculating stress:
    if Keys.STRESS in property_labels:
        # The virial stress tensor is the gradient of the total energy wrt
        # an infinitesimal change in the cell parameters.
        # We therefore add this change to the cell, such that
        # we can calculate the gradient wrt later if required.
        #
        # See <> TODO: find reference
        actual_cell = structure.cell
        change_to_cell = torch.zeros_like(actual_cell, requires_grad=True)
        symmetric_change = 0.5 * (
            change_to_cell + change_to_cell.transpose(-1, -2)
        )
        structure.cell = actual_cell + symmetric_change
    else:
        change_to_cell = torch.zeros_like(structure.cell)

    # use the autograd machinery to auto-magically calculate forces and stress
    # from the energy
    with require_grad(structure._positions), require_grad(change_to_cell):
        energy = pes(structure)

        if Keys.ENERGY in property_labels:
            predictions[property_labels[Keys.ENERGY]] = energy

        if Keys.FORCES in property_labels:
            dE_dR = differentiate(energy, structure._positions)
            predictions[property_labels[Keys.FORCES]] = -dE_dR

        if Keys.STRESS in property_labels:
            stress = differentiate(energy, change_to_cell)
            predictions[property_labels[Keys.STRESS]] = stress

    return predictions
