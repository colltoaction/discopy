from pytest import raises
from discopy.markov import Ty as MarkovTy
from discopy.closed import Ty as ClosedTy
from discopy.monoidal import Ty as MonoidalTy
from discopy.rigid import Ty as RigidTy

def test_mixed_types_tensor():
    # Setup
    c = ClosedTy('x')
    m = MarkovTy(c)

    # Check what MarkovTy is now
    assert issubclass(MarkovTy, ClosedTy)

    # Test 1: MonoidalTy (as MarkovTy) @ ClosedTy
    # MarkovTy is now ClosedTy.
    # m @ c -> ClosedTy @ ClosedTy.
    res1 = m @ c
    assert isinstance(res1, ClosedTy)
    assert res1.inside[0] == c
    assert res1.inside[1] == c.inside[0]

    # Test 2: ClosedTy @ MonoidalTy (as MarkovTy)
    # c @ m -> ClosedTy @ ClosedTy.
    res2 = c @ m
    assert isinstance(res2, ClosedTy)
    assert res2.inside[0] == c.inside[0]
    assert res2.inside[1] == c

    # Test 3: RigidTy @ ClosedTy (Sub1 @ Sub2)
    # r @ c.
    # RigidTy vs ClosedTy. Strict check fails (or init check).
    # Strict check: assert_isinstance(other, self.factory).
    # Closed is not Rigid.
    # So r @ c should fail in tensor check.
    r = RigidTy('r')
    with raises(TypeError) as excinfo:
        r @ c
    # Error message depends on which check fails.
    # "Expected rigid.Ty, got closed.Ty instead"
    assert "Expected" in str(excinfo.value)

    # Test 4: ClosedTy @ RigidTy (Super @ Sub)
    # c @ r.
    # self=Closed. other=Rigid.
    # other is Closed. OK.
    # self is Rigid? No.
    # Strict check fails.
    with raises(TypeError):
        c @ r

    # Test 5: RigidTy @ MarkovTy
    # r @ m.
    # Rigid vs Closed.
    # Fails.
    with raises(TypeError):
        r @ m

    # Test 6: MarkovTy @ RigidTy
    # m @ r.
    # Closed vs Rigid.
    # Fails.
    with raises(TypeError):
        m @ r
