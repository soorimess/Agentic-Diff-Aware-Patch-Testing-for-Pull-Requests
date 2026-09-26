"""Test that posify preserves assumptions on symbols."""

from sympy import Symbol, posify


def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption on symbols."""
    x = Symbol('x', finite=True)
    
    # Check that x has the finite assumption before posify
    assert x.is_finite is True
    assert x._assumptions['finite'] is True
    
    # Apply posify
    xp, rep = posify(x)
    
    # Check that xp preserves the finite assumption
    assert xp.is_finite is True
    assert xp._assumptions['finite'] is True


def test_posify_preserves_nonfinite_assumption():
    """Test that posify preserves non-finite assumptions."""
    x = Symbol('x', finite=False)
    
    # Check that x has the finite assumption before posify
    assert x.is_finite is False
    assert x._assumptions['finite'] is False
    
    # Apply posify
    xp, rep = posify(x)
    
    # Check that xp preserves the finite assumption
    assert xp.is_finite is False
    assert xp._assumptions['finite'] is False


def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions on symbols."""
    x = Symbol('x', finite=True, integer=True, positive=True)
    
    # Check that x has all assumptions before posify
    assert x.is_finite is True
    assert x.is_integer is True
    assert x.is_positive is True
    
    # Apply posify
    xp, rep = posify(x)
    
    # Check that xp preserves all assumptions
    assert xp.is_finite is True
    assert xp.is_integer is True
    assert xp.is_positive is True