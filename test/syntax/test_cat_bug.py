from discopy.cat import Ob, Box, Functor, Arrow
import pytest

def test_functor_then_bug():
    x = Ob('x')
    f = Box('f', x, x)

    # Case 1: ar returns raw data (tuple of boxes)
    # F maps f to (f,) which is converted to Arrow((f,), x, x) by F.__call__
    F = Functor({x: x}, {f: (f,)})
    G = Functor.id()

    # This should not raise TypeError
    try:
        H = F.then(G)
    except TypeError:
        pytest.fail("Functor.then failed with raw data in ar mapping")

    assert H(f) == f

    # Case 2: ob returns raw data (string)
    # F2 maps x to "y". "y" is converted to Ob("y") by F2.__call__
    y = Ob('y')
    # Note: we need to ensure F2 is well-defined. F2(x)=y.
    # We map f to Box('g', y, y).
    F2 = Functor({x: "y"}, {f: Box('g', y, y)})

    # This should not raise TypeError
    try:
        H2 = F2.then(G)
    except TypeError:
        pytest.fail("Functor.then failed with raw data in ob mapping")

    assert H2(x) == y
