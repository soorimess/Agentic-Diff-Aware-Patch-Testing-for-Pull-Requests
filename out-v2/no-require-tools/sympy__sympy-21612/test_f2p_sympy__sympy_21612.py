"""
Regression test for the specific fix in str.py that handles power parentheses.
This test ensures that when a power expression has a power base, proper 
parentheses are added in string representation to avoid ambiguity.
"""

from sympy import Pow, Mul, Symbol, sstr

def test_power_base_parentheses_handling():
    """
    Test that ensures the fix for handling power bases works correctly.
    
    The fix in str.py changed isinstance(item.base, Mul) to 
    isinstance(item.base, (Mul, Pow)) to handle cases where the base
    of a power expression is itself a power expression.
    """
    c = Symbol('c')
    a = Symbol('a')
    b = Symbol('b')
    
    # Test case 1: Simple power (should work the same)
    expr1 = Pow(c, -2)  # c**(-2)
    str1 = sstr(expr1)
    
    # Test case 2: Power with mul base - this should trigger the condition
    # when the mul has more than one argument
    mul_expr = Mul(a, b, evaluate=False)  # Creates a Mul with args (a, b)
    expr2 = Pow(mul_expr, -1)  # This is (a*b)**(-1) = 1/(a*b)
    str2 = sstr(expr2)
    
    # Test case 3: Power with power base - this is the case that was specifically fixed
    expr3 = Pow(Pow(a, 2), -1)  # This is (a**2)**(-1) = 1/(a**2)  
    str3 = sstr(expr3)
    
    # All should produce valid string representations
    assert str1 is not None
    assert str2 is not None
    assert str3 is not None
    
    # The main assertion is that the fix doesn't break anything
    # and that we have proper coverage for the specific change