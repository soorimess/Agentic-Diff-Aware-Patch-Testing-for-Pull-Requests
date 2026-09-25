"""Test for posify assumption preservation bug."""

from sympy import Symbol, posify


def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption of symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Verify the original symbol has the finite assumption
    assert x.is_finite is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should also preserve the finite assumption
    # Before the fix, this would return None instead of True
    assert xp.is_finite is True


def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions of symbols."""
    # Create a symbol with multiple assumptions
    x = Symbol('x', finite=True, integer=True)
    
    # Verify the original symbol has the assumptions
    assert x.is_finite is True
    assert x.is_integer is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should preserve the assumptions
    assert xp.is_finite is True
    assert xp.is_integer is True


def test_posify_preserves_real_assumption():
    """Test that posify preserves the real assumption of symbols."""
    # Create a symbol with real=True assumption
    x = Symbol('x', real=True)
    
    # Verify the original symbol has the real assumption
    assert x.is_real is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should preserve the real assumption
    assert xp.is_real is True