from sympy import Function
from sympy.utilities.lambdify import implemented_function


def test_evalf_of_composed_implemented_functions():
    # Implement two simple numerical functions:
    f = Function('f')
    g = Function('g')
    f = implemented_function(f, lambda x: x**2)
    g = implemented_function(g, lambda x: 2*x)

    # sanity checks
    assert f(2).evalf() == 4
    assert g(2).evalf() == 4

    # The composition should evaluate numerically. Before the fix this
    # returned the unevaluated expression f(g(2)). After the fix it should
    # return 16.
    assert f(g(2)).evalf() == 16

    # clean up
    del f._imp_
    del g._imp_
