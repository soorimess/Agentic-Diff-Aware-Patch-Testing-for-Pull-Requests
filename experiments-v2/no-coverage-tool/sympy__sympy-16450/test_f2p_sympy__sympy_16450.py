"""Test that posify preserves assumptions like finite."""

from sympy import Symbol, posify, Dummy


def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption on symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Verify the symbol has the finite assumption
    assert x.is_finite is True
    assert x._assumptions['finite'] is True
    
    # Apply posify
    xp, rep = posify(x)
    
    # The new symbol should preserve the finite assumption
    # Before the fix, xp.is_finite would be None (not preserved)
    # After the fix, xp.is_finite should be True (preserved)
    assert xp.is_finite is True
    assert xp._assumptions['finite'] is True
    
    # The new symbol should also be positive (as required by posify)
    assert xp.is_positive is True
    assert xp._assumptions['positive'] is True


def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions."""
    # Create a symbol with multiple assumptions
    x = Symbol('x', finite=True, integer=True, positive=True)
    
    # Verify the symbol has the assumptions
    assert x.is_finite is True
    assert x.is_integer is True
    assert x.is_positive is True
    
    # Apply posify
    xp, rep = posify(x)
    
    # The new symbol should preserve all assumptions
    assert xp.is_finite is True
    assert xp.is_integer is True
    assert xp.is_positive is True
    assert xp._assumptions['finite'] is True
    assert xp._assumptions['integer'] is True
    assert xp._assumptions['positive'] is True


def test_posify_creates_positive_dummy():
    """Test that posify creates a positive dummy symbol."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Apply posify
    xp, rep = posify(x)
    
    # The new symbol should be a Dummy with positive=True
    assert isinstance(xp, Dummy)
    assert xp.is_positive is True
    assert xp._assumptions['positive'] is True