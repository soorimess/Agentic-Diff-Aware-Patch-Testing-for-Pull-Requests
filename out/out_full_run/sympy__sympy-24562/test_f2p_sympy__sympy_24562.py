from sympy.core.numbers import Rational


def test_rational_with_string_numerator_and_denominator():
    # Regression test for sympy/sympy#24562: when both numerator and
    # denominator are given as strings (e.g. '0.5', '100') the old
    # implementation could perform string repetition ("100" * 2 ->
    # "100100") leading to an incorrect Rational of 1/100100.
    # The expected correct value for Rational('0.5', '100') is 1/200.
    r = Rational('0.5', '100')
    assert r.p == 1 and r.q == 200
    assert r == Rational(1, 200)
