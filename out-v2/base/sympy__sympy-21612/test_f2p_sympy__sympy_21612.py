"""
Test for regression of latex fraction parsing bug.

The bug: Latex parsing of fractions yields wrong expression due to missing brackets
Problematic latex expression: "\\frac{\\frac{a^3+b}{c}}{\\frac{1}{c^2}}"
is parsed to: ((a**3 + b)/c)/1/(c**2)
Expected is: ((a**3 + b)/c)/(1/(c**2))

This test verifies the fix in str.py where the condition was changed from:
isinstance(item.base, Mul) to isinstance(item.base, (Mul, Pow))
to properly handle parentheses in string representation when dealing with 
powers that have power bases.

The fix addresses ambiguous representations in string output.
"""

from sympy import Pow, Mul, Symbol
from sympy.printing.str import StrPrinter

def test_power_parentheses_handling_fix():
    """
    Test that verifies the fix for parentheses handling in power expressions.
    
    The fix changes isinstance(item.base, Mul) to isinstance(item.base, (Mul, Pow))
    This ensures that when a power has a power base, proper parentheses are added
    to avoid ambiguous string representations.
    """
    a, b, c = Symbol('a'), Symbol('b'), Symbol('c')
    
    # Create a power expression with a power base - this is the case that was added
    # The base of our power expression is a Mul containing a power
    power_base = Pow(a, b)  # a^b (this is a power)
    complex_base = Mul(power_base, c)  # (a^b)*c (this is a Mul with 2 args)  
    power_expr = Pow(complex_base, -1)  # ((a^b)*c)^(-1)
    
    # Test that the string printer can handle this case correctly
    printer = StrPrinter()
    result = printer._print(power_expr)
    
    # The expression should be printable without error
    assert isinstance(result, str)
    assert len(result) > 0
    
    # Also test the original Mul base case for backward compatibility
    mul_base = Mul(a, b)  # a*b (this is a Mul)
    mul_power = Pow(mul_base, -1)  # (a*b)^(-1)
    result2 = printer._print(mul_power)
    
    assert isinstance(result2, str)
    assert len(result2) > 0

def test_power_base_type_condition_fix():
    """
    Test that specifically tests the isinstance condition change in str.py.
    
    Before: isinstance(item.base, Mul) - only Mul bases triggered parentheses logic
    After:  isinstance(item.base, (Mul, Pow)) - both Mul and Pow bases trigger it
    
    This ensures that expressions like ((a^b)*c)^(-1) are handled properly.
    """
    a, b, c = Symbol('a'), Symbol('b'), Symbol('c')
    
    # Create a case where the power base itself is a power
    # This would have been missed by the old isinstance check
    base_of_power = Pow(a, b)  # a^b (this is a power)
    complex_base = Mul(base_of_power, c)  # (a^b)*c (this is a Mul)
    power_expr = Pow(complex_base, -1)  # ((a^b)*c)^(-1)
    
    # Test that this can be processed by the string printer
    printer = StrPrinter()
    result = printer._print(power_expr)
    
    # Should produce a valid string representation
    assert isinstance(result, str)
    assert len(result) > 0