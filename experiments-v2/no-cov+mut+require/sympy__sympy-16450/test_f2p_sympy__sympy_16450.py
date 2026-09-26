from sympy import Symbol, posify

def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption of symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Check that it initially has the finite assumption
    assert x.is_finite is True
    assert 'finite' in x._assumptions
    assert x._assumptions['finite'] is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # After posify, the new symbol should still preserve the finite assumption
    # Before the fix, this would return None (missing assumption)
    # After the fix, this should return True
    assert xp.is_finite is True, "posify should preserve finite assumption"
    
    # Also check that other assumptions are preserved
    assert 'finite' in xp._assumptions
    assert xp._assumptions['finite'] is True

def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions including finite."""
    # Create a symbol with multiple assumptions
    x = Symbol('x', finite=True, integer=True, positive=True)
    
    # Check initial assumptions
    assert x.is_finite is True
    assert x.is_integer is True
    assert x.is_positive is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # Check that all assumptions are preserved
    assert xp.is_finite is True, "posify should preserve finite assumption"
    assert xp.is_integer is True, "posify should preserve integer assumption"
    assert xp.is_positive is True, "posify should preserve positive assumption"
    
    # Check that the assumptions dict contains the preserved values
    assert 'finite' in xp._assumptions
    assert 'integer' in xp._assumptions
    assert 'positive' in xp._assumptions
    assert xp._assumptions['finite'] is True
    assert xp._assumptions['integer'] is True
    assert xp._assumptions['positive'] is True

def test_posify_preserves_nonfinite_assumption():
    """Test that posify preserves non-finite assumptions."""
    # Create a symbol with finite=False assumption (infinite)
    x = Symbol('x', finite=False)
    
    # Check initial assumptions
    assert x.is_finite is False
    assert 'finite' in x._assumptions
    assert x._assumptions['finite'] is False
    
    # Apply posify
    xp, _ = posify(x)
    
    # Check that finite assumption is preserved
    assert xp.is_finite is False, "posify should preserve finite=False assumption"
    assert 'finite' in xp._assumptions
    assert xp._assumptions['finite'] is False