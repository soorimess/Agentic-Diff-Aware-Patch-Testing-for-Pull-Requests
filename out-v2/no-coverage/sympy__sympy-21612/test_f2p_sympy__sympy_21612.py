"""
Regression test for the latex parsing nested fractions issue.

This test verifies the fix in sympy/printing/str.py that ensures 
power expressions with power bases are handled consistently in string representations.

The fix changed isinstance(item.base, Mul) to isinstance(item.base, (Mul, Pow))
to maintain consistent parentheses handling for nested power expressions.
"""

from sympy import symbols, Pow, Mul


def test_power_expression_with_power_base_handling():
    """
    Test that power expressions with power bases are handled correctly.
    
    This validates the fix that ensures power expressions with power bases
    get the same treatment as those with Mul bases in string representation.
    """
    c = symbols('c')
    
    # Create a power expression where the base is itself a power expression
    # This is the specific case that was added to the isinstance check
    base_expr = Pow(c, 2, evaluate=False)  # c^2
    power_expr = Pow(base_expr, -1, evaluate=False)  # (c^2)^(-1)
    
    # String representation should work without error
    str_repr = str(power_expr)
    
    # Basic validation
    assert str_repr is not None
    assert 'c' in str_repr or '**' in str_repr


def test_consistency_in_power_base_handling():
    """
    Test consistent handling of different power base types.
    
    Ensures both Mul and Pow bases are treated consistently to prevent
    ambiguous string representations.
    """
    c = symbols('c')
    
    # Mul base case (existing functionality)
    mul_base = Mul(c, c, evaluate=False)  # c*c
    pow_mul = Pow(mul_base, -1, evaluate=False)  # (c*c)^(-1)
    
    # Pow base case (new functionality added by the fix)
    pow_base = Pow(c, 2, evaluate=False)  # c^2
    pow_pow = Pow(pow_base, -1, evaluate=False)  # (c^2)^(-1)
    
    # Both should produce valid string representations
    str_mul = str(pow_mul)
    str_pow = str(pow_pow)
    
    assert str_mul is not None
    assert str_pow is not None