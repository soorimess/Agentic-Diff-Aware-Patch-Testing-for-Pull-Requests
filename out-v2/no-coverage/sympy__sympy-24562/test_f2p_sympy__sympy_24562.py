"""Test for Rational calculation bug with string inputs."""

from sympy import Rational

def test_rational_string_inputs():
    """Test that Rational('0.5', '100') and Rational(0.5, 100) behave consistently."""
    # The bug: Rational('0.5', '100') returns 1/100100 instead of 1/200
    # while Rational(0.5, 100) returns 1/200 correctly
    
    # Test the problematic case
    result1 = Rational('0.5', '100')
    expected1 = Rational(1, 200)  # This should be the correct result
    
    # Test the working case for comparison
    result2 = Rational(0.5, 100)
    expected2 = Rational(1, 200)  # This should be the correct result
    
    # Both should be equal to 1/200
    assert result1 == expected1, f"Rational('0.5', '100') = {result1}, expected {expected1}"
    assert result2 == expected2, f"Rational(0.5, 100) = {result2}, expected {expected2}"
    
    # They should be equal to each other
    assert result1 == result2, f"Rational('0.5', '100') = {result1} != Rational(0.5, 100) = {result2}"