"""
Test for Rational calc value error bug.

Bug report: 
when calc Rational('0.5', '100'), the value is 1/100100; 
but Rational(0.5, 100) the value is 1/200, this value is the true value, 
and the version of sympy 1.8 is normal
"""

from sympy import Rational

def test_rational_string_consistency():
    """Test that Rational with string arguments behaves consistently"""
    # Both should return the same correct value: 1/200
    # The bug was that Rational('0.5', '100') returned 1/100100 instead of 1/200
    
    result1 = Rational('0.5', '100')
    result2 = Rational(0.5, 100)
    result3 = Rational('0.5', 100)
    result4 = Rational(0.5, '100')
    
    expected = Rational(1, 200)
    
    # All should be equal to the correct value
    assert result1 == expected, f"Rational('0.5', '100') should be {expected}, got {result1}"
    assert result2 == expected, f"Rational(0.5, 100) should be {expected}, got {result2}"
    assert result3 == expected, f"Rational('0.5', 100) should be {expected}, got {result3}"
    assert result4 == expected, f"Rational(0.5, '100') should be {expected}, got {result4}"
    
    # The main assertion: all should be equal to each other
    assert result1 == result2 == result3 == result4, \
        f"All results should be equal: {result1}, {result2}, {result3}, {result4}"