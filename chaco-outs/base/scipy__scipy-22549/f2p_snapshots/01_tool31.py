"""
Regression test for PR #22549: ENH: use `workers` keyword in `optimize._differentiable_functions.VectorFunction`

This test ensures that the `workers` keyword argument is properly handled in VectorFunction
when computing Jacobians via finite differences.
"""
import numpy as np
from scipy.optimize._differentiable_functions import VectorFunction
from scipy.optimize._hessian_update_strategy import BFGS
from scipy._lib._util import MapWrapper


def test_vector_function_workers_parameter_exists():
    """Test that VectorFunction accepts the workers parameter without error."""
    
    # Define a simple vector function
    def vector_func(x):
        return np.array([x[0]**2 + x[1], x[0] * x[1]])
    
    # Test data
    x0 = np.array([1.0, 2.0])
    
    # This should work without error (the main test for the PR)
    # Using compatible parameters: finite diff jac + callable hess
    vf = VectorFunction(vector_func, x0, jac='3-point', hess=BFGS(),
                        finite_diff_rel_step=None, finite_diff_jac_sparsity=None,
                        finite_diff_bounds=(-np.inf, np.inf), sparse_jacobian=None, workers=None)
    
    # Should be able to compute Jacobian
    J = vf.jac(x0)  # Note: jac() requires x parameter
    
    # Should compute without error
    assert J.shape == (2, 2)
    assert vf.nfev > 0


def test_vector_function_workers_with_map_wrapper():
    """Test that VectorFunction works with MapWrapper as workers."""
    
    # Define a simple vector function
    def vector_func(x):
        return np.array([x[0]**2 + x[1], x[0] * x[1]])
    
    # Test data
    x0 = np.array([1.0, 2.0])
    
    # Test with MapWrapper as workers
    vf = VectorFunction(vector_func, x0, jac='3-point', hess=BFGS(),
                        finite_diff_rel_step=None, finite_diff_jac_sparsity=None,
                        finite_diff_bounds=(-np.inf, np.inf), sparse_jacobian=None, workers=MapWrapper())
    
    # Should compute Jacobian without error
    J = vf.jac(x0)
    assert J.shape == (2, 2)
    assert vf.nfev > 0


def test_vector_function_workers_with_workers_none():
    """Test that VectorFunction works with workers=None (default)."""
    
    # Define a simple vector function
    def vector_func(x):
        return np.array([x[0]**2 + x[1], x[0] * x[1]])
    
    # Test data
    x0 = np.array([1.0, 2.0])
    
    # Test with workers=None explicitly
    vf = VectorFunction(vector_func, x0, jac='3-point', hess=BFGS(),
                        finite_diff_rel_step=None, finite_diff_jac_sparsity=None,
                        finite_diff_bounds=(-np.inf, np.inf), sparse_jacobian=None, workers=None)
    
    # Should compute Jacobian without error
    J = vf.jac(x0)
    assert J.shape == (2, 2)
    assert vf.nfev > 0


if __name__ == "__main__":
    test_vector_function_workers_parameter_exists()
    test_vector_function_workers_with_map_wrapper()
    test_vector_function_workers_with_workers_none()
    print("All tests passed!")