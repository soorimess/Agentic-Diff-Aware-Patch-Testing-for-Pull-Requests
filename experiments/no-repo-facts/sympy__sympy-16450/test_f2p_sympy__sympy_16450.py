"""
Regression test for posify finite assumption preservation.
This test makes sure that posify preserves the finite assumption when creating dummy symbols.
"""

from sympy import Symbol, posify, sqrt


def test_posify_finite_assumption():
    """Test that posify preserves finite assumption."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Apply posify
    xp, _ = posify(x)
    
    # The new symbol should preserve the finite assumption
    assert xp.is_finite is True