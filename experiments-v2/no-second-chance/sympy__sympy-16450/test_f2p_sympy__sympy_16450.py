from sympy import Symbol, posify

def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption of symbols.
    
    This is a regression test for the bug where posify would remove finite 
    assumptions from symbols.
    """
    # Create a symbol with finite=True assumption (as shown in the bug report)
    x = Symbol('x', finite=True)
    
    # Verify the original symbol has the finite assumption
    assert x.is_finite is True
    assert x._assumptions['finite'] is True
    
    # Apply posify - this should preserve the finite assumption
    xp, _ = posify(x)
    
    # The new symbol should preserve the finite assumption (this was broken before the fix)
    assert xp.is_finite is True
    assert xp._assumptions['finite'] is True