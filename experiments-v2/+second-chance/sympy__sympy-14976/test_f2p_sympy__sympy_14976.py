"""Test for the bug where lambdify(modules='mpmath') doesn't wrap rationals."""

from sympy.printing.pycode import MpmathPrinter
from sympy import Rational


def test_mpmath_rational_handling():
    """Test that MpmathPrinter properly handles Rational numbers."""
    # The fix adds _print_Rational method to MpmathPrinter to wrap rationals in mpmath.mpf()
    # Before fix: Rational(2, 3) -> '2/3' (no precision)
    # After fix: Rational(2, 3) -> 'mpmath.mpf(2)/mpmath.mpf(3)' (with precision)
    
    printer = MpmathPrinter()
    
    # Test the specific behavior that the fix enables
    r = Rational(2, 3)
    
    # This test should fail before the fix is applied (when method doesn't work properly)
    # and pass after the fix is applied (when method works correctly)
    try:
        result = printer._print_Rational(r)
        
        # The fix should make this return a mpmath-formatted string
        # If it returns just '2/3', the fix is not working properly
        if result == '2/3':
            # This indicates the bug is present - method not properly implemented
            # This test should fail in the buggy state
            raise AssertionError("Rational not properly wrapped in mpmath calls")
        else:
            # Method works correctly - returns mpmath-formatted result
            assert 'mpmath.mpf' in result
            assert '2' in result and '3' in result
            
    except AttributeError:
        # Method doesn't exist yet - this is the bug state
        # This test should fail before the fix
        raise AssertionError("MpmathPrinter._print_Rational method not found - fix not applied")