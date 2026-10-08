from sympy.core.numbers import Rational

def test_rational_string_multiplication_bug():
    """Test for Rational calculation error with string inputs that caused string multiplication.
    
    When Rational('0.5', '100') was called, it incorrectly performed string 
    multiplication instead of integer multiplication, resulting in denominator 100100
    instead of 200.
    """
    # This should return 1/200 (the correct value)
    result1 = Rational(0.5, 100)
    assert result1 == Rational(1, 200)
    
    # This was incorrectly returning 1/100100 due to string multiplication bug
    result2 = Rational('0.5', '100') 
    assert result2 == Rational(1, 200)
    
    # Additional test cases to make sure we cover the fix properly
    # Test with other string combinations that could trigger similar issues
    result3 = Rational('0.25', '4') 
    assert result3 == Rational(1, 16)
    
    result4 = Rational('0.1', '10')
    assert result4 == Rational(1, 100)