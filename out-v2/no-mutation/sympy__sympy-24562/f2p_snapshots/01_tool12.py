from sympy.core.numbers import Rational

def test_rational_string_string_bug():
    """Test for bug where Rational('0.5', '100') gave wrong result.
    
    The bug was that when both arguments to Rational are strings,
    the denominator was incorrectly calculated due to string multiplication
    instead of numeric multiplication.
    """
    # This should give 1/200 (the correct mathematical result)
    result = Rational('0.5', '100')
    expected = Rational(1, 200)
    
    # The bug caused this to return 1/100100 instead of 1/200
    assert result == expected

def test_rational_float_int_consistency():
    """Test that Rational(0.5, 100) and Rational('0.5', '100') give same result.
    
    This ensures consistency between string and non-string arguments.
    """
    r1 = Rational(0.5, 100)
    r2 = Rational('0.5', '100')
    
    # Both should give the same correct result: 1/200
    assert r1 == r2 == Rational(1, 200)