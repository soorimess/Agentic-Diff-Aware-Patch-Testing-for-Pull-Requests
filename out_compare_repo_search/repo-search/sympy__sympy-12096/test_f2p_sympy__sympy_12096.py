from sympy.utilities.lambdify import implemented_function


def test_sympy_12096_evalf_calls_imp_recursively():
    """Regression test for issue #12096: evalf should evaluate
    implemented functions' arguments before calling _imp_.
    """
    # Create two implemented (numerical) functions:
    f = implemented_function('f', lambda x: x**2)
    g = implemented_function('g', lambda x: 2 * x)

    # Basic sanity checks: single applications evaluate
    assert f(2).evalf() == 4
    assert g(2).evalf() == 4

    # The composed application should also evaluate to a numeric value.
    # With the bug present this would return the unevaluated expression
    # f(g(2)) instead of 16
    assert f(g(2)).evalf() == 16

    # Clean up the injected implementations so other tests are unaffected
    try:
        del f._imp_
    except Exception:
        pass
    try:
        del g._imp_
    except Exception:
        pass
