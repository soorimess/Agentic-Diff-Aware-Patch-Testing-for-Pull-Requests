"""
Test for regression of posify ignoring is_finite assumptions
"""

from sympy import Symbol, posify, Dummy


def test_posify_preserves_finite_assumption():
    """
    Test that posify preserves the finite assumption on symbols.
    
    Before the fix: posify would remove the finite assumption from symbols
    After the fix: posify should preserve all assumptions from the original symbol
    """
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Verify the symbol has the finite assumption before posify
    assert x.is_finite is True
    assert x._assumptions['finite'] is True
    
    # Apply posify
    xp, rep = posify(x)
    
    # After posify, the new dummy symbol should preserve finite assumption
    # Before the fix: xp.is_finite would be None
    # After the fix: xp.is_finite should be True
    assert xp.is_finite is True
    assert xp._assumptions['finite'] is True


def test_posify_preserves_multiple_assumptions():
    """
    Test that posify preserves multiple assumptions on symbols.
    
    The fix should preserve all assumptions from the original symbol.
    """
    # Create a symbol with multiple assumptions
    x = Symbol('x', finite=True, integer=True, positive=True)
    
    # Verify assumptions before posify
    assert x.is_finite is True
    assert x.is_integer is True
    assert x.is_positive is True
    
    # Apply posify
    xp, rep = posify(x)
    
    # After posify, the new dummy symbol should preserve all assumptions
    assert xp.is_finite is True
    assert xp.is_integer is True
    assert xp.is_positive is True


def test_posify_preserves_assumptions_with_non_positive_symbols():
    """
    Test posify behavior when symbols don't have positive=None
    """
    # Create a symbol with positive=True assumption (should not be replaced by posify)
    x_pos = Symbol('x', positive=True)
    
    # This should not be replaced since is_positive is not None
    xp, rep = posify(x_pos)
    
    # Since it was already positive, it should remain unchanged
    assert xp == x_pos
    assert len(rep) == 0


def test_posify_preserves_assumptions_with_no_restrictions():
    """
    Test posify behavior with regular symbol that has no assumptions.
    """
    # Create a regular symbol with no specific assumptions
    x = Symbol('x')
    
    # No assumptions to begin with
    assert x.is_finite is None
    assert x.is_integer is None
    
    # Apply posify
    xp, rep = posify(x)
    
    # Should create new dummy with positive=True only (no additional assumptions)
    # posify will create a dummy with positive=True. 
    assert xp.is_positive is True  # The point of posify
    assert xp._assumptions.get('finite') is None  # This should be None, not preserved from original
    # The current behavior is that it's not preserved since Symbol has no assumptions


def test_original_bug_case():
    """
    Test the exact case from the bug report
    """
    x = Symbol('x', finite=True)
    
    # Check initial assumptions
    assert x._assumptions['finite'] is True
    
    # Apply posify
    xp, _ = posify(x)
    
    # This assertion should pass after fix, fail before fix
    # Before fix, xp.is_finite would be None
    # After fix, xp.is_finite should be True
    assert xp.is_finite is True