"""
Regression test for the string representation issue with nested power expressions.

This test ensures that when a Power expression has another Power as its base,
parentheses are properly added in the string representation to maintain
mathematical clarity.
"""

from sympy import symbols, Pow
from sympy.printing.str import sstr

def test_nested_power_string_representation():
    """
    Test that nested power expressions get proper parentheses in string representation.
    
    The fix in str.py changed the condition from isinstance(item.base, Mul) 
    to isinstance(item.base, (Mul, Pow)) to ensure that when a Power has a 
    Power as its base, parentheses are added to make the structure clear.
    
    Before the fix: (a**b)**c would display as a**b**c (without parentheses)
    After the fix: (a**b)**c would display as (a**b)**c (with parentheses)
    """
    a, b, c = symbols('a b c')
    
    # Create a nested power expression: (a**b)**c
    # This should now get parentheses in its string representation with the fix
    nested_pow = Pow(Pow(a, b, evaluate=False), c, evaluate=False)
    str_repr = sstr(nested_pow)
    
    # The fix ensures that when the base of a Pow is itself a Pow,
    # parentheses are added to make the structure clear
    expected = "(a**b)**c"
    assert str_repr == expected, f"String representation mismatch: expected {expected}, got {str_repr}"

def test_mul_power_string_representation():
    """
    Test that Mul-based power expressions still work correctly (preserving old behavior).
    
    This ensures the original functionality for Mul bases is preserved.
    """
    a, b, c = symbols('a b c')
    
    # Create a power expression with Mul base: (a*b)**c
    mul_pow = Pow(a*b, c, evaluate=False)
    str_repr = sstr(mul_pow)
    
    # Should still have parentheses around the base
    expected = "(a*b)**c"
    assert str_repr == expected, f"String representation mismatch: expected {expected}, got {str_repr}"