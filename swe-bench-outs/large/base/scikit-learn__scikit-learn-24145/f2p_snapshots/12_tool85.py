"""Tests for the SplineTransformer sparse output functionality.

This test file verifies the behavior of SplineTransformer with sparse_output=True
as introduced in the pull request.
"""

import numpy as np
import pytest
from sklearn.preprocessing import SplineTransformer


def test_spline_transformer_sparse_output_parameter_exists():
    """Test that SplineTransformer accepts sparse_output parameter."""
    # This test should fail before the PR (because parameter doesn't exist)
    # and pass after the PR (because parameter exists)
    
    # Test that sparse_output parameter exists and can be set to False
    spline = SplineTransformer(degree=2, n_knots=3, sparse_output=False)
    assert hasattr(spline, 'sparse_output')
    assert spline.sparse_output is False
    
    # Test that sparse_output parameter can be set to True  
    spline = SplineTransformer(degree=2, n_knots=3, sparse_output=True)
    assert spline.sparse_output is True


def test_spline_transformer_sparse_output_parameter_in_signature():
    """Test that sparse_output parameter is in the __init__ signature."""
    # This test should fail before the PR (because parameter doesn't exist)
    # and pass after the PR (because parameter is in signature)
    
    import inspect
    sig = inspect.signature(SplineTransformer.__init__)
    params = list(sig.parameters.keys())
    
    # Check that sparse_output is in the parameters
    assert 'sparse_output' in params


def test_spline_transformer_sparse_output_default_value():
    """Test that sparse_output defaults to False."""
    # This test should fail before the PR (because parameter doesn't exist)
    # and pass after the PR (because parameter exists and defaults to False)
    
    # Test that sparse_output defaults to False
    spline = SplineTransformer(degree=2, n_knots=3)
    assert hasattr(spline, 'sparse_output')
    assert spline.sparse_output is False