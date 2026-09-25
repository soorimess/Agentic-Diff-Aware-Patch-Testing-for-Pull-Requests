"""Test that posify preserves finite assumptions."""

from sympy import Symbol, posify


def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption of symbols."""
    x = Symbol('x', finite=True)
    
    # Check the original symbol has finite=True
    assert x.is_finite is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should also have is_finite=True
    # This is what the fix ensures - before the fix this would be None
    assert xp.is_finite is True
    
    # The new symbol should still be positive (required for posify functionality)
    assert xp.is_positive is True


def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions including finite."""
    x = Symbol('x', finite=True, integer=True)
    
    # Check the original symbol has assumptions
    assert x.is_finite is True
    assert x.is_integer is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should preserve both assumptions
    assert xp.is_finite is True
    assert xp.is_integer is True
    
    # The new symbol should still be positive (required for posify functionality)
    assert xp.is_positive is True


def test_posify_preserves_non_finite():
    """Test that posify preserves non-finite assumptions correctly."""
    x = Symbol('x', finite=False)
    
    # Check the original symbol has finite=False
    assert x.is_finite is False
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should also have is_finite=False
    assert xp.is_finite is False
    
    # The new symbol should still be positive (required for posify functionality)
    assert xp.is_positive is True


def test_posify_preserves_other_assumptions():
    """Test that posify preserves other assumptions like rational, even, etc."""
    x = Symbol('x', finite=True, rational=True, even=True)
    
    # Check the original symbol has assumptions
    assert x.is_finite is True
    assert x.is_rational is True
    assert x.is_even is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should preserve all assumptions
    assert xp.is_finite is True
    assert xp.is_rational is True
    assert xp.is_even is True
    
    # The new symbol should still be positive (required for posify functionality)
    assert xp.is_positive is True