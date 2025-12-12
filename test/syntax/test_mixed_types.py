from pytest import raises
from discopy.markov import Ty as MarkovTy
from discopy.closed import Ty as ClosedTy
from discopy.monoidal import Ty as MonoidalTy
from discopy.rigid import Ty as RigidTy

def test_mixed_types_tensor():
    # Setup
    c = ClosedTy('x')
    m = MarkovTy(c) # MarkovTy is MonoidalTy, so this is MonoidalTy(ClosedTy('x'))
    # m contains c as an atomic object. c contains Ob('x').

    # Check factories
    assert m.factory == MonoidalTy
    assert c.factory == ClosedTy
    assert issubclass(ClosedTy, MonoidalTy)

    # Test 1: MonoidalTy @ ClosedTy (Super @ Sub)
    # Should work and return MonoidalTy (Super)
    # m is MonoidalTy. c is ClosedTy.
    # isinstance(c, MonoidalTy) is True.
    res1 = m @ c
    assert isinstance(res1, MonoidalTy)
    assert not isinstance(res1, ClosedTy)
    # m.inside is (c,). c.inside is (Ob('x'),).
    # res1.inside is (c, Ob('x'))
    assert len(res1.inside) == 2
    assert res1.inside[0] == c
    assert res1.inside[1] == c.inside[0]

    # Test 2: ClosedTy @ MonoidalTy (Sub @ Super)
    # This implies downcasting MonoidalTy to ClosedTy.
    # isinstance(m, ClosedTy) is False.
    # Should FAIL.

    with raises(TypeError):
        c @ m

    # Test 3: RigidTy @ ClosedTy (Sub1 @ Sub2) - Incompatible (unsafe downcast)
    # RigidTy is subclass of ClosedTy.
    # r @ c.
    # isinstance(c, RigidTy) is False.
    # Should FAIL.

    r = RigidTy('r')

    with raises(TypeError):
        r @ c

    # Test 4: ClosedTy @ RigidTy (Super @ Sub)
    # c @ r.
    # isinstance(r, ClosedTy) is True.
    # Should WORK.
    res_cr = c @ r
    assert isinstance(res_cr, ClosedTy)
    assert not isinstance(res_cr, RigidTy)

    # Test 5: RigidTy @ MonoidalTy (Sub @ Super)
    # r @ m.
    # isinstance(m, RigidTy) is False.
    # Should FAIL.
    with raises(TypeError):
        r @ m

    # Test 6: MonoidalTy @ RigidTy (Super @ Sub)
    # m @ r.
    # isinstance(r, MonoidalTy) is True.
    # Should WORK.
    res4 = m @ r
    assert isinstance(res4, MonoidalTy)
    assert res4.inside[0] == c
    assert res4.inside[1] == r.inside[0]
