from discopy.markov import Ty, Diagram

def test_markov_ty_factory_mismatch():
    """
    This test reproduces a bug where markov.Diagram.ty_factory defaulted to monoidal.Ty
    while markov.Ty was changed to closed.Ty.

    Diagram.copy calls frobenius.spiders, which calls cls.id().
    If cls.id() returns a diagram with monoidal.Ty, but we tensor it with closed.Ty objects,
    strict type checking in monoidal.Ty.tensor raises a TypeError.
    """
    x = Ty('x')
    # This should not raise TypeError
    Diagram.copy(x)
