"""Tests for posify assumption preservation."""

from sympy import Symbol, posify


def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption of symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should preserve the finite assumption
    assert xp.is_finite is True


def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions of symbols."""
    # Create a symbol with multiple assumptions
    x = Symbol('x', finite=True, integer=True)
    
    # Apply posify
    xp, _ = posify(x)
    
    # Both assumptions should be preserved
    assert xp.is_finite is True
    assert xp.is_integer is True


def test_posify_preserves_assumptions_with_positive_symbol():
    """Test that posify preserves assumptions even for already positive symbols."""
    # Create a symbol that is already positive
    x = Symbol('x', positive=True, finite=True)
    
    # Apply posify
    xp, _ = posify(x)
    
    # Assumptions should be preserved
    assert xp.is_positive is True
    assert xp.is_finite is True