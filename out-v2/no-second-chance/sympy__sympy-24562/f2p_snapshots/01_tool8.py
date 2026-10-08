"""
Regression test for Rational calc value error.

Bug report: when calc Rational('0.5', '100'), the value is 1/100100; 
but Rational(0.5, 100) the value is 1/200, this value is the true value, 
and the version of sympy 1.8 is normal
"""

def test_rational_string_args():
    """Test that Rational('0.5', '100') returns 1/200, not 1/100100"""
    from sympy import Rational
    
    # This should return 1/200, not 1/100100
    r1 = Rational('0.5', '100')
    assert r1 == Rational(1, 200), f"Expected 1/200, got {r1}"
    
    # This should return 1/200 (same result as above)
    r2 = Rational(0.5, 100)
    assert r2 == Rational(1, 200), f"Expected 1/200, got {r2}"
    
    # Verify they are equal
    assert r1 == r2, f"Rational('0.5', '100') and Rational(0.5, 100) should be equal"