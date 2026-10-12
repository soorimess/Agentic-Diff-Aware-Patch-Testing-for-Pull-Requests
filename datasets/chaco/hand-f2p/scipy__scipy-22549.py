import numpy as np
from numpy.testing import assert_allclose

from scipy.optimize._differentiable_functions import VectorFunction


def fun(x):
    return np.array([x[0] ** 2 + x[1], np.sin(x[0]) * x[1]])


def jac(x):
    return np.array([[2 * x[0], 1.0], [np.cos(x[0]) * x[1], np.sin(x[0])]])


def hess(x, v):
    return (v[0] * np.array([[2.0, 0.0], [0.0, 0.0]])
            + v[1] * np.array([[-np.sin(x[0]) * x[1], np.cos(x[0])],
                               [np.cos(x[0]), 0.0]]))


def test_vector_function_finite_differences_with_workers():
    # Finite-difference evaluations can be spread over a map-like `workers`.
    x0 = np.array([0.5, 2.0])
    for scheme in ("2-point", "3-point"):
        vf = VectorFunction(fun, x0, scheme, hess, None, None, (-np.inf, np.inf),
                            False, workers=map)
        serial = VectorFunction(fun, x0, scheme, hess, None, None, (-np.inf, np.inf),
                                False)
        assert_allclose(vf.jac(x0), jac(x0), rtol=1e-5, atol=1e-6)
        assert vf.nfev == serial.nfev
