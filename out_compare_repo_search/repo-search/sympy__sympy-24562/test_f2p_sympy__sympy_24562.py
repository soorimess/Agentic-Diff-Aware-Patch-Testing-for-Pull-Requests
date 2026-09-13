# Regression test for sympy/sympy#24562
# Ensure that passing strings for numerator and denominator yields the
# mathematically expected Rational value.

def test_rational_string_numerator_and_denominator():
    from sympy import Rational

    # Before the fix this produced 1/100100 because the string denominator
    # was inadvertently repeated when multiplied by the numerator's q.
    # The correct value is 1/200.
    assert Rational('0.5', '100') == Rational(1, 200)

    # Sanity check: the mixed (float, int) case has long been correct.
    assert Rational(0.5, 100) == Rational(1, 200)
