"""Test for posify assumption preservation bug."""

from sympy import Symbol, posify


def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption on symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Check that the original symbol has the finite assumption
    assert x.is_finite is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should preserve the finite assumption
    # Before the fix, this would be None (assumption lost)
    # After the fix, this should be True
    assert xp.is_finite is True


def test_posify_preserves_infinite_assumption():
    """Test that posify preserves the infinite assumption."""
    # Create a symbol with infinite=True assumption
    x = Symbol('x', infinite=True)
    
    # Check that the original symbol has the infinite assumption
    assert x.is_infinite is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should preserve the infinite assumption
    assert xp.is_infinite is True