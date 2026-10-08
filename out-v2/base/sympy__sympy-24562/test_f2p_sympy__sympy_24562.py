"""
Regression test for Rational calc value error.

The bug was that Rational('0.5', '100') returned 1/100100 instead of 1/200.
This was caused by a change in how the denominator was computed when both
arguments are strings.
"""

def test_rational_string_args_bug():
    """Test that Rational('0.5', '100') returns the correct value."""
    from sympy import Rational
    
    # This should return 1/200 (the correct value)
    result = Rational('0.5', '100')
    expected = Rational(1, 200)
    
    # The bug was that this returned 1/100100 instead of 1/200
    assert result == expected, f"Expected {expected}, got {result}"

def test_rational_float_args():
    """Test that Rational(0.5, 100) still works correctly."""
    from sympy import Rational
    
    # This should return 1/200 (the correct value)  
    result = Rational(0.5, 100)
    expected = Rational(1, 200)
    
    assert result == expected, f"Expected {expected}, got {result}"