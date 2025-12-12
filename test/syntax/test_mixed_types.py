from pytest import raises
from discopy.markov import Ty as MarkovTy
from discopy.closed import Ty as ClosedTy
from discopy.monoidal import Ty as MonoidalTy
from discopy.rigid import Ty as RigidTy

def test_mixed_types_tensor():
    # Setup
    c = ClosedTy('x')
    m = MarkovTy(c)

    # Test 1: MonoidalTy @ ClosedTy (Super @ Sub)
    # m is MonoidalTy (Ambiguous=True). c is ClosedTy (Ambiguous=True).
    # Allowed.
    res1 = m @ c
    assert isinstance(res1, MonoidalTy)
    assert not isinstance(res1, ClosedTy)
    assert res1.inside[0] == c
    assert res1.inside[1] == c.inside[0]

    # Test 2: ClosedTy @ MonoidalTy (Sub @ Super)
    # c @ m.
    # Allowed because of ambiguous inheritance.
    res2 = c @ m
    assert isinstance(res2, ClosedTy)
    assert res2.inside[0] == c.inside[0]
    assert res2.inside[1] == c

    # Test 3: RigidTy @ ClosedTy (Sub1 @ Sub2)
    # r @ c.
    # Allowed by tensor assertion (ambiguous), BUT fails in RigidTy.__init__
    # because ClosedTy objects are not RigidTy objects.
    r = RigidTy('r')
    with raises(TypeError) as excinfo:
        r @ c
    assert "Expected str | rigid.Ob, got cat.Ob instead" in str(excinfo.value)

    # Test 4: ClosedTy @ RigidTy (Super @ Sub)
    # c @ r.
    # Allowed. Rigid objects are Ob, so valid in ClosedTy.
    res4 = c @ r
    assert isinstance(res4, ClosedTy)

    # Test 5: RigidTy @ MonoidalTy (Sub @ Super)
    # r @ m.
    # Allowed by tensor assertion.
    # m contains c. c is Ty (Ob).
    # c is NOT RigidTy object (does not have .l/.r unless casted?).
    # RigidTy checks if objects are rigid.Ob.
    # c is Ty, which is cat.Ob. Is it rigid.Ob? No.
    # So r @ m should also fail in __init__.
    with raises(TypeError) as excinfo:
        r @ m
    assert "Expected str | rigid.Ob, got closed.Ty instead" in str(excinfo.value) or "Expected str | rigid.Ob, got monoidal.Ty instead" in str(excinfo.value) or "Expected str | rigid.Ob, got cat.Ob instead" in str(excinfo.value)

    # Test 6: MonoidalTy @ RigidTy (Super @ Sub)
    # m @ r.
    # Allowed.
    res6 = m @ r
    assert isinstance(res6, MonoidalTy)
