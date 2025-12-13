import pytest
from discopy import balanced, braided, traced, compact, quantum

def test_balanced_diagram_mro():
    """ Verify the MRO of balanced.Diagram is as expected. """
    mro = balanced.Diagram.mro()
    assert balanced.Diagram in mro
    assert braided.Diagram in mro
    assert traced.Diagram in mro
    # braided comes before traced in balanced.Diagram definition
    assert mro.index(braided.Diagram) < mro.index(traced.Diagram)

def test_mro_conflict_reproduction():
    """
    Demonstrate that mixing classes with conflicting MROs raises TypeError.
    balanced.Diagram inherits (braided.Diagram, traced.Diagram).
    If we mix it with a class inheriting (traced.Diagram, braided.Diagram), it should fail.
    """
    class AntiBalancedDiagram(traced.Diagram, braided.Diagram):
        pass

    with pytest.raises(TypeError, match="Cannot create a consistent method resolution"):
        class Conflict(balanced.Diagram, AntiBalancedDiagram):
            pass

def test_complex_hierarchy_consistency():
    """ Verify that complex classes like quantum.circuit.Box have a resolvable MRO. """
    try:
        mro = quantum.circuit.Box.mro()
        # Verify some key precedence rules
        # quantum.circuit.Box -> ... -> compact.Box
        assert quantum.circuit.Box in mro
        assert compact.Box in mro

        # compact.Box -> symmetric.Box, ribbon.Box
        assert mro.index(compact.Box) < mro.index(balanced.Box)

    except Exception as e:
        pytest.fail(f"MRO check failed: {e}")

def test_box_vs_diagram_mro():
    """
    Check MRO consistency between Box and Diagram in balanced category.
    balanced.Box inherits (braided.Box, traced.Box, balanced.Diagram).
    This implies braided.Box < traced.Box.
    balanced.Diagram inherits (braided.Diagram, traced.Diagram).
    This implies braided.Diagram < traced.Diagram.

    Since braided.Box depends on braided.Diagram and traced.Box on traced.Diagram,
    the order matches.
    """
    box_mro = balanced.Box.mro()
    assert box_mro.index(braided.Box) < box_mro.index(traced.Box)
    assert box_mro.index(balanced.Diagram) > box_mro.index(traced.Box)
