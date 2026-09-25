from sympy.utilities.lambdify import implemented_function


def test_evalf_calls_imp_recursively():
    """Regression test for sympy/sympy#12096: evalf should call the
    implementation (_imp_) with evaluated numeric arguments so that composed
    implemented functions are evaluated correctly.
    """
    f = implemented_function('f', lambda x: x**2)
    g = implemented_function('g', lambda x: 2 * x)

    # simple cases work
    assert f(2).evalf() == 4.0
    assert g(2).evalf() == 4.0

    # the composition used to *not* evaluate because args were not
    # passed through evalf() before calling _imp_. The correct result is 16.0
    # (i.e. f(g(2)) -> f(4) -> 16)
    assert f(g(2)).evalf() == 16.0
