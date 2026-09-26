"""Test for posify ignoring is_finite assumptions."""

from sympy import Symbol, posify


def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption of symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Verify the assumption is set correctly before posify
    assert x.is_finite is True
    assert x._assumptions['finite'] is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should preserve the finite assumption
    # Before the fix, this would return None instead of True
    assert xp.is_finite is True


def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions including finite."""
    # Create a symbol with multiple assumptions
    x = Symbol('x', finite=True, integer=True)
    
    # Verify assumptions before posify
    assert x.is_finite is True
    assert x.is_integer is True
    assert x._assumptions['finite'] is True
    assert x._assumptions['integer'] is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should preserve both assumptions
    assert xp.is_finite is True
    assert xp.is_integer is True


def test_posify_still_makes_symbol_positive():
    """Test that posify still makes the symbol positive as intended."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should still be positive (core functionality)
    assert xp.is_positive is True