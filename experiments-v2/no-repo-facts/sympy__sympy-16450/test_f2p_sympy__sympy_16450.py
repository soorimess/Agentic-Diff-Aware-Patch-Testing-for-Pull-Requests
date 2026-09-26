from sympy import Symbol, posify

def test_posify_preserves_finiteness():
    """Test that posify preserves the finite assumption of symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Verify the initial assumptions
    assert x.is_finite is True
    assert x._assumptions['finite'] is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # The bug: posify removes the finite assumption from _assumptions dict
    # After the fix, this should still be True
    # Note: is_finite might still be None due to how assumptions are processed,
    # but the key point is that finite should be preserved in the assumptions dict
    assert 'finite' in xp._assumptions
    assert xp._assumptions['finite'] is True


def test_posify_preserves_integer_assumption():
    """Test that posify preserves the integer assumption of symbols."""
    # Test with integer assumption
    y = Symbol('y', integer=True)
    yp, _ = posify(y)
    assert yp.is_integer is True, "posify should preserve the integer assumption"


def test_posify_preserves_rational_assumption():
    """Test that posify preserves the rational assumption of symbols."""
    # Test with rational assumption
    z = Symbol('z', rational=True)
    zp, _ = posify(z)
    assert zp.is_rational is True, "posify should preserve the rational assumption"