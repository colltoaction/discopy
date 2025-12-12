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
    # m is MonoidalTy. c is ClosedTy.
    # self=Monoidal. other=Closed.
    # self in (Closed, Monoidal). True.
    # other in Monoidal. True.
    # Allowed.
    res1 = m @ c
    assert isinstance(res1, MonoidalTy)
    assert not isinstance(res1, ClosedTy)
    assert res1.inside[0] == c
    assert res1.inside[1] == c.inside[0]

    # Test 2: ClosedTy @ MonoidalTy (Sub @ Super)
    # c @ m.
    # self=Closed. other=Monoidal.
    # other in Closed? False.
    # Should FAIL.
    with raises(TypeError):
        c @ m

    # Test 3: RigidTy @ ClosedTy (Sub1 @ Sub2)
    # r @ c.
    # self=Rigid. other=Closed.
    # other in Rigid? False.
    # Should FAIL.
    r = RigidTy('r')
    with raises(TypeError):
        r @ c

    # Test 4: ClosedTy @ RigidTy (Super @ Sub)
    # c @ r.
    # self=Closed. other=Rigid.
    # self in (Rigid, Closed). True.
    # other in Closed. True.
    # Allowed.
    res4 = c @ r
    assert isinstance(res4, ClosedTy)

    # Test 5: RigidTy @ MonoidalTy (Sub @ Super)
    # r @ m.
    # other=Monoidal. self=Rigid.
    # other in Rigid? False.
    # Should FAIL.
    with raises(TypeError):
        r @ m

    # Test 6: MonoidalTy @ RigidTy (Super @ Sub)
    # m @ r.
    # self=Monoidal. other=Rigid.
    # self in (Rigid, Monoidal). True.
    # other in Monoidal. True.
    # Allowed.
    res6 = m @ r
    assert isinstance(res6, MonoidalTy)
