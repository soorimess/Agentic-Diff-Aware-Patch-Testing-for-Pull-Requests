from sympy.core.numbers import Rational

def test_rational_string_args():
    """Test for bug where Rational('0.5', '100') produces wrong result."""
    # This should produce 1/200, not 1/100100
    result1 = Rational('0.5', '100')
    expected1 = Rational(1, 200)
    print(f"Rational('0.5', '100') = {result1}")
    print(f"Expected: {expected1}")
    print(f"Are they equal? {result1 == expected1}")
    
    # This should also produce 1/200 (the working case)
    result2 = Rational(0.5, 100)
    expected2 = Rational(1, 200)
    print(f"Rational(0.5, 100) = {result2}")
    print(f"Expected: {expected2}")
    print(f"Are they equal? {result2 == expected2}")
    
    # Make sure both give the same result
    print(f"Are result1 and result2 equal? {result1 == result2}")
    
    assert result1 == expected1
    assert result2 == expected2
    assert result1 == result2