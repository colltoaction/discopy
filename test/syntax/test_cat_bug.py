from discopy.cat import Ob, Box, Functor, Arrow
import pytest

def test_functor_then_bug():
    x, y, z = Ob('x'), Ob('y'), Ob('z')
    f = Box('f', x, y)
    g = Box('g', y, z)
    h = Box('h', z, z)

    # Case 1: ar returns raw data (tuple of boxes)
    # F maps f to (f,) which is syntactic sugar for Arrow((f,), x, y)
    F = Functor({x: x, y: y}, {f: (f,)})

    # G maps f to g. This ensures G receives the converted Arrow(f),
    # matches it against the key f (if F output the correct object), and maps it to g.
    # Note: Functor dictionary keys are Boxes.
    # If F outputs Arrow((f,)...) and G expects Box('f'...),
    # G.ar[Box('f'..)] should match?
    # Wait, G.ar is {f: g}. f is a Box.
    # F(f) returns Arrow((f,),...). Arrow is not equal to Box?
    # Box IS an Arrow.
    # But Arrow((f,)) == f (the Box) is True.
    # So G(F(f)) should work if F(f) == f.

    G = Functor({x: y, y: z}, {f: g})

    # This should not raise TypeError
    try:
        H = F.then(G)
    except TypeError:
        pytest.fail("Functor.then failed with raw data in ar mapping")

    # H(f) = G(F(f)) = G(f) = g
    assert H(f) == g


    # Case 2: ob returns raw data (string)
    # F2 maps x to "y". "y" is converted to Ob("y") by F2.__call__
    F2 = Functor({x: "y", y: "z"}, {f: g})

    # G2 maps y to z.
    # F2(x) should be Ob("y") (y).
    # G2(y) should be z.
    G2 = Functor({y: z, z: z}, {g: h})

    # This should not raise TypeError
    try:
        H2 = F2.then(G2)
    except TypeError:
        pytest.fail("Functor.then failed with raw data in ob mapping")

    assert H2(x) == z
    assert H2(f) == h
