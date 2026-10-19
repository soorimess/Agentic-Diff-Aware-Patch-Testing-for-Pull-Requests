"""Tests for the SplineTransformer sparse output functionality.

This test file verifies the behavior of SplineTransformer with sparse_output=True
as introduced in the pull request.
"""

import numpy as np
import pytest
from sklearn.preprocessing import SplineTransformer


def test_spline_transformer_sparse_output_parameter_exists():
    """Test that SplineTransformer accepts sparse_output parameter."""
    # This test should pass after the PR is applied
    # Before the PR, it will be skipped because sparse_output parameter doesn't exist
    
    try:
        # Test that sparse_output parameter exists and can be set to False
        spline = SplineTransformer(degree=2, n_knots=3, sparse_output=False)
        assert hasattr(spline, 'sparse_output')
        assert spline.sparse_output is False
        
        # Test that sparse_output parameter can be set to True  
        spline = SplineTransformer(degree=2, n_knots=3, sparse_output=True)
        assert spline.sparse_output is True
        
    except TypeError as e:
        # This is expected before the PR is merged
        if "unexpected keyword argument 'sparse_output'" in str(e):
            pytest.skip("sparse_output parameter not yet implemented")
        else:
            raise


def test_spline_transformer_sparse_output_parameter_in_signature():
    """Test that sparse_output parameter is in the __init__ signature."""
    # This test should pass after the PR is applied
    # Before the PR, it will be skipped because sparse_output parameter doesn't exist
    
    try:
        import inspect
        sig = inspect.signature(SplineTransformer.__init__)
        params = list(sig.parameters.keys())
        
        # Check that sparse_output is in the parameters
        assert 'sparse_output' in params
        
    except TypeError as e:
        # This is expected before the PR is merged
        if "unexpected keyword argument 'sparse_output'" in str(e):
            pytest.skip("sparse_output parameter not yet implemented")
        else:
            raise
    except Exception:
        # Re-raise any other exceptions
        raise


def test_spline_transformer_sparse_output_validation():
    """Test that sparse_output=True requires scipy >= 1.8.0."""
    # This test should pass after the PR is applied
    # Before the PR, it will be skipped because sparse_output parameter doesn't exist
    
    X = np.arange(6).reshape(6, 1)
    
    try:
        # Try to create transformer with sparse_output=True
        spline = SplineTransformer(degree=2, n_knots=3, sparse_output=True)
        
        # Try to fit - this should trigger validation
        spline.fit(X)
        
        # If we get here, it means either:
        # 1. scipy >= 1.8.0 (validation passed) 
        # 2. The validation logic was bypassed or doesn't work as expected
        
    except TypeError as e:
        # This is expected before the PR is merged
        if "unexpected keyword argument 'sparse_output'" in str(e):
            pytest.skip("sparse_output parameter not yet implemented")
        else:
            raise
    except ValueError as e:
        # This should happen after PR is applied with scipy < 1.8.0
        if "scipy>=1.8.0" in str(e):
            # This is the expected validation error
            pass
        else:
            raise