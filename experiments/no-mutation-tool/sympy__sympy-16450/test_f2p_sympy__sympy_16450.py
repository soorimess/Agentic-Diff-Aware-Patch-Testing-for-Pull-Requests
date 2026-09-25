"""Tests for posify assumption preservation"""

from sympy import Symbol, posify


def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption on symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Verify the original symbol has the assumption
    assert x.is_finite is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # After posify, the new symbol should also preserve the finite assumption
    # This is the expected behavior after the fix
    assert xp.is_finite is True


def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions on symbols."""
    # Create a symbol with multiple assumptions
    x = Symbol('x', finite=True, integer=True, positive=True)
    
    # Verify the original symbol has the assumptions
    assert x.is_finite is True
    assert x.is_integer is True
    assert x.is_positive is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # After posify, the new symbol should preserve all assumptions
    assert xp.is_finite is True
    assert xp.is_integer is True
    assert xp.is_positive is True


def test_posify_preserves_nonfinite_assumption():
    """Test that posify preserves non-finite assumptions."""
    # Create a symbol with finite=False assumption 
    x = Symbol('x', finite=False)
    
    # Verify the original symbol has the assumption
    assert x.is_finite is False
    
    # Apply posify
    xp, _ = posify(x)
    
    # After posify, the new symbol should also preserve the finite assumption
    assert xp.is_finite is False