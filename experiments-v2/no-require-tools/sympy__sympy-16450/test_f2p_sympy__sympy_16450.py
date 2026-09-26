"""Test that posify preserves assumptions like finite."""

from sympy import Symbol, posify


def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption on symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Verify the assumption is set correctly before posify
    assert x.is_finite is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should preserve the finite assumption
    assert xp.is_finite is True


def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions."""
    # Create a symbol with multiple assumptions
    x = Symbol('x', finite=True, integer=True)
    
    # Verify the assumptions are set correctly before posify
    assert x.is_finite is True
    assert x.is_integer is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should preserve both assumptions
    assert xp.is_finite is True
    assert xp.is_integer is True


def test_posify_still_creates_positive_symbol():
    """Test that posify still creates a positive symbol."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should still be positive (this is the main purpose of posify)
    assert xp.is_positive is True