"""Test that posify preserves assumptions like finite."""

from sympy import Symbol, posify

def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption of symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Verify the symbol initially has the finite assumption
    assert x.is_finite is True
    assert x._assumptions['finite'] is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # Test that the new symbol preserves the finite assumption
    assert xp.is_finite is True
    assert xp._assumptions['finite'] is True


def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions."""
    # Create a symbol with multiple assumptions
    x = Symbol('x', finite=True, integer=True, positive=True)
    
    # Verify the symbol initially has the assumptions
    assert x.is_finite is True
    assert x.is_integer is True
    assert x.is_positive is True
    assert x._assumptions['finite'] is True
    assert x._assumptions['integer'] is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # Test that the new symbol preserves the assumptions
    assert xp.is_finite is True
    assert xp.is_integer is True
    assert xp.is_positive is True
    assert xp._assumptions['finite'] is True
    assert xp._assumptions['integer'] is True


def test_posify_preserves_nonfinite_assumption():
    """Test that posify preserves non-finite assumptions.""" 
    # Create a symbol with finite=False assumption
    x = Symbol('x', finite=False)
    
    # Verify the symbol initially has the finite assumption
    assert x.is_finite is False
    assert x._assumptions['finite'] is False
    
    # Apply posify
    xp, _ = posify(x)
    
    # Test that the new symbol preserves the finite assumption
    assert xp.is_finite is False
    assert xp._assumptions['finite'] is False


def test_posify_preserves_nonpositive_assumption():
    """Test that posify preserves non-positive assumptions."""
    # Create a symbol with positive=False assumption
    x = Symbol('x', positive=False)
    
    # Verify the symbol initially has the positive assumption
    assert x.is_positive is False
    assert x._assumptions['positive'] is False
    
    # Apply posify
    xp, _ = posify(x)
    
    # Test that the new symbol preserves the positive assumption
    assert xp.is_positive is False
    assert xp._assumptions['positive'] is False


def test_posify_preserves_infinite_assumption():
    """Test that posify preserves the infinite assumption."""
    # Create a symbol with infinite=True assumption  
    x = Symbol('x', infinite=True)
    
    # Verify the symbol initially has the infinite assumption
    assert x.is_infinite is True
    assert x._assumptions['infinite'] is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # Test that the new symbol preserves the infinite assumption
    assert xp.is_infinite is True
    assert xp._assumptions['infinite'] is True