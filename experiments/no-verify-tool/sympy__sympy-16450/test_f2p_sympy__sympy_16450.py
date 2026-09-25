"""Test for posify preserving assumptions like finite."""

from sympy import Symbol, posify


def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption on symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Verify the initial assumption
    assert x.is_finite is True
    assert x._assumptions['finite'] is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # Before the fix, xp would lose the finite assumption
    # After the fix, xp should preserve the finite assumption
    assert xp.is_finite is True
    assert xp._assumptions['finite'] is True


def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions on symbols."""
    # Create a symbol with multiple assumptions
    x = Symbol('x', finite=True, integer=True)
    
    # Verify the initial assumptions
    assert x.is_finite is True
    assert x.is_integer is True
    assert x._assumptions['finite'] is True
    assert x._assumptions['integer'] is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # Check that assumptions are preserved
    assert xp.is_finite is True
    assert xp.is_integer is True
    assert xp._assumptions['finite'] is True
    assert xp._assumptions['integer'] is True