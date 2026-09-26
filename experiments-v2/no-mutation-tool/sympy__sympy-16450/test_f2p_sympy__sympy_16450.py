"""Test for posify ignoring is_finite assumptions."""

from sympy import Symbol, posify


def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption of symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Verify the symbol has the finite assumption
    assert x.is_finite is True
    assert x._assumptions['finite'] is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # Before the fix, xp would lose the finite assumption
    # After the fix, xp should preserve the finite assumption
    assert xp.is_finite is True
    assert xp._assumptions['finite'] is True