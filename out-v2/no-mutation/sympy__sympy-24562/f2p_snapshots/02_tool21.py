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

def test_rational_consistency_between_string_and_float():
    """Test that Rational(0.5, 100) and Rational('0.5', '100') give same result.
    
    This ensures consistency between string and non-string arguments.
    """
    r1 = Rational(0.5, 100)
    r2 = Rational('0.5', '100')
    
    # Both should give the same correct result: 1/200
    assert r1 == r2 == Rational(1, 200)

def test_rational_string_string_different_values():
    """Test another case to ensure the fix works generally."""
    # Test with different values to make sure the fix is robust
    result = Rational('0.25', '50')
    expected = Rational(1, 200)  # 0.25/50 = 1/4 / 50 = 1/200
    
    assert result == expected