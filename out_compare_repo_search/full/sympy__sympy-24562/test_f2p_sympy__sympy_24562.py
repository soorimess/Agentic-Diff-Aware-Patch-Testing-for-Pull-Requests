from sympy import Rational


def test_rational_string_numerator_and_denominator():
    # Regression test for sympy/sympy#24562:
    # Rational('0.5', '100') should parse both string inputs
    # and produce 1/200 (not 1/100100 which was produced before).
    r = Rational('0.5', '100')
    assert r == Rational(1, 200)
    assert r.p == 1 and r.q == 200
