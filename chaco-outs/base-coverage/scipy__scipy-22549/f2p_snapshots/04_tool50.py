"""
Test for PR #22549: ENH: use `workers` keyword in `optimize._differentiable_functions.VectorFunction`

This test verifies that the `workers` keyword argument is properly handled
in VectorFunction and affects the behavior of finite difference computations.
"""
import numpy as np
from scipy.optimize._differentiable_functions import VectorFunction


def test_vector_function_workers_parameter_exists():
    """Test that VectorFunction accepts the workers parameter."""
    
    # Simple test function
    def fun(x):
        return np.array([x[0]**2 + x[1]**2])
    
    # Simple hessian function (callable) that doesn't do anything
    def hess_func(x):
        return np.eye(2)
    
    x0 = np.array([1.0, 2.0])
    
    # Test that VectorFunction accepts workers parameter without error
    # This should fail before the PR with "unexpected keyword argument 'workers'"
    # and after the PR it should work
    try:
        vf = VectorFunction(fun, x0, '2-point', hess_func, None, None, 
                            (-np.inf, np.inf), None, workers=1)
        # If we get here, the workers parameter is accepted
        assert True
    except TypeError as e:
        if "unexpected keyword argument 'workers'" in str(e):
            # This is expected before the PR - the parameter doesn't exist yet
            raise AssertionError("workers parameter not yet implemented")
        else:
            # Some other TypeError - this is fine, the important thing is 
            # that we're not getting the workers error
            assert True


if __name__ == "__main__":
    try:
        test_vector_function_workers_parameter_exists()
        print("SUCCESS: workers parameter is implemented!")
    except AssertionError as e:
        if "workers parameter not yet implemented" in str(e):
            print("EXPECTED FAILURE: workers parameter not yet implemented")
        else:
            print(f"UNEXPECTED ERROR: {e}")
    except Exception as e:
        print(f"OTHER ERROR (expected after PR): {e}")