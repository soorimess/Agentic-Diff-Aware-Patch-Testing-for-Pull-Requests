"""Test that posify preserves assumptions including is_finite."""

from sympy import Symbol, posify


def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Verify the symbol has the finite assumption
    assert x.is_finite is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should also have the finite assumption preserved
    # This would fail before the fix
    assert xp.is_finite is True


def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions including finite."""
    # Create a symbol with multiple assumptions including finite
    x = Symbol('x', finite=True, integer=True)
    
    # Verify assumptions
    assert x.is_finite is True
    assert x.is_integer is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # Both assumptions should be preserved
    assert xp.is_finite is True
    assert xp.is_integer is True


def test_posify_preserves_nonfinite_assumption():
    """Test that posify preserves the non-finite assumption as well."""
    # Create a symbol with finite=False assumption (i.e. infinite)
    x = Symbol('x', finite=False)
    
    # Verify the symbol has the finite assumption set to False
    assert x.is_finite is False
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should also have the finite assumption preserved
    assert xp.is_finite is False


def test_posify_preserves_other_assumptions():
    """Test that posify preserves other assumptions like positive, negative, etc."""
    # Create a symbol with various assumptions 
    x = Symbol('x', finite=True, positive=True, integer=True)
    
    # Verify assumptions
    assert x.is_finite is True
    assert x.is_positive is True
    assert x.is_integer is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # All assumptions should be preserved
    assert xp.is_finite is True
    assert xp.is_positive is True
    assert xp.is_integer is True