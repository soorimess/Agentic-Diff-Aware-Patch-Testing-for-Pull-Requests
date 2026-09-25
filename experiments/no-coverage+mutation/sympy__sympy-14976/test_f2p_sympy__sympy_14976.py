"""
Test for the Rational handling in mpmath lambdification
This test verifies that rationals are properly converted to mpmath.mpf for precision
"""
from sympy import Rational
from sympy.printing.pycode import MpmathPrinter

def test_mpmath_rational_conversion():
    """Test that Rational numbers are properly converted to mpmath.mpf in mpmath printer"""
    # Create a rational number
    r = Rational(232, 3)
    
    # Test with MpmathPrinter directly 
    printer = MpmathPrinter()
    result = printer.doprint(r)
    
    # This test directly verifies the specific change:
    # Before the fix, this would return "232/3"  
    # After the fix, it should return "mpmath.mpf(232)/mpmath.mpf(3)"
    expected = "mpmath.mpf(232)/mpmath.mpf(3)"
    
    assert expected == result, f"Expected {expected}, got {result}"