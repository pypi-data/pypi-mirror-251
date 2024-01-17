import numpy as np
import pytest
import torch
from graph_pes.util import (
    as_possible_tensor,
    differentiate,
    pairs,
    require_grad,
    shape_repr,
    to_chem_symbol,
)


def test_pairs():
    assert list(pairs([1, 2, 3])) == [(1, 2), (2, 3)]


def test_shape_repr():
    d = dict(
        a=torch.rand(1, 2),
        b=torch.rand(1),
    )
    assert shape_repr(d) == "a=[1,2], b=[1]"


def test_to_chem_symbol():
    assert to_chem_symbol(1) == "H"
    assert to_chem_symbol(6) == "C"
    assert to_chem_symbol(118) == "Og"


possible_tensors = [
    (1, True),
    (1.0, True),
    ([1, 2, 3], True),
    (torch.tensor([1, 2, 3]), True),
    (np.array([1, 2, 3]), True),
    (np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64), True),
    ("hello", False),
]


@pytest.mark.parametrize("obj, can_be_converted", possible_tensors)
def test_as_possible_tensor(obj, can_be_converted):
    if can_be_converted:
        assert isinstance(as_possible_tensor(obj), torch.Tensor)
    else:
        assert as_possible_tensor(obj) is None


def test_require_grad():
    # first, check that sensible error messages are displayed if attempting
    # to use this in a no_grad context:
    with torch.no_grad(), pytest.raises(
        RuntimeError, match="calculate gradients"
    ):
        x = torch.zeros(1)
        with require_grad(x):
            pass

    # now check that this thing actually works:
    y = torch.zeros(1, requires_grad=False)
    with require_grad(y):
        assert y.requires_grad
    assert not y.requires_grad

    z = torch.zeros(1, requires_grad=True)
    with require_grad(z):
        assert z.requires_grad
    assert z.requires_grad


def test_get_gradient():
    # test nice error message
    x = torch.tensor([1.0, 2.0, 3.0])
    y = x.sum()
    with pytest.raises(ValueError, match="must be the result of a computation"):
        dy_dx = differentiate(y, x)

    # test that it works
    x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    y = x.sum()
    dy_dx = differentiate(y, x)
    assert torch.allclose(dy_dx, torch.ones_like(x))

    # test that it works with a non-scalar y
    x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    y = x**2
    dy_dx = differentiate(y, x)
    assert torch.allclose(dy_dx, 2 * x)

    # test that it works if x is not part of the computation graph
    x = torch.tensor([1.0, 2.0, 3.0])
    z = torch.tensor([4.0, 5.0, 6.0], requires_grad=True)
    y = z.sum()
    dy_dx = differentiate(y, x)
    assert torch.allclose(dy_dx, torch.zeros_like(x))

    # finally, we want to test that the gradient itself has a gradient
    x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    y = (x**2).sum()
    dy_dx = differentiate(y, x)
    dy_dx2 = differentiate(dy_dx, x)
    assert torch.allclose(dy_dx2, 2 * torch.ones_like(x))
