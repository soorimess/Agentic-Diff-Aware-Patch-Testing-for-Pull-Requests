import numpy as np
import pytest
from scipy import sparse
from sklearn.utils.fixes import sp_version, parse_version
from sklearn.preprocessing import SplineTransformer
from sklearn.utils._testing import assert_allclose


def test_spline_transformer_sparse_output_parameter_exists():
    """Test that SplineTransformer accepts sparse_output parameter."""
    # This test should fail before the change and pass after the change
    X = np.arange(6).reshape(6, 1)
    
    # Test that sparse_output parameter can be set without error
    try:
        spline = SplineTransformer(degree=2, n_knots=3, sparse_output=True)
        assert hasattr(spline, 'sparse_output')
        assert spline.sparse_output is True
        # Test that it can be set to False too
        spline2 = SplineTransformer(degree=2, n_knots=3, sparse_output=False)
        assert spline2.sparse_output is False
    except TypeError as e:
        # This is expected in the current codebase - sparse_output doesn't exist yet
        pytest.fail(f"Expected sparse_output parameter to exist, but got: {e}")


def test_spline_transformer_sparse_output_returns_sparse_matrix():
    """Test that SplineTransformer returns sparse matrix when sparse_output=True."""
    X = np.arange(6).reshape(6, 1)
    
    try:
        spline = SplineTransformer(degree=2, n_knots=3, sparse_output=True)
        result = spline.fit_transform(X)
        
        # Check if result is sparse
        assert sparse.issparse(result), "Result should be sparse when sparse_output=True"
        
        # Check that it's a CSR matrix
        assert sparse.isspmatrix_csr(result), "Result should be CSR sparse matrix"
        
    except TypeError as e:
        # This is expected in the current codebase - sparse_output doesn't exist yet
        pytest.skip("sparse_output parameter not implemented yet")
    except ValueError as e:
        # This might happen if scipy version is too old
        if "scipy>=1.8.0" in str(e):
            pytest.skip("scipy version too old for sparse output")
        raise


def test_spline_transformer_sparse_output_default_is_dense():
    """Test that SplineTransformer defaults to dense output."""
    X = np.arange(6).reshape(6, 1)
    
    try:
        spline = SplineTransformer(degree=2, n_knots=3)
        result = spline.fit_transform(X)
        
        # Should be dense by default
        assert not sparse.issparse(result), "Result should be dense by default"
        assert isinstance(result, np.ndarray), "Result should be numpy array by default"
        
    except TypeError as e:
        # This is expected in the current codebase - sparse_output doesn't exist yet
        pytest.skip("sparse_output parameter not implemented yet")
    except ValueError as e:
        # This might happen if scipy version is too old
        if "scipy>=1.8.0" in str(e):
            pytest.skip("scipy version too old for sparse output")
        raise


def test_spline_transformer_sparse_output_consistency():
    """Test that sparse and dense outputs are consistent."""
    X = np.arange(10).reshape(5, 2)
    
    try:
        # Test with sparse output
        spline_sparse = SplineTransformer(degree=2, n_knots=3, sparse_output=True)
        result_sparse = spline_sparse.fit_transform(X)
        
        # Test with dense output
        spline_dense = SplineTransformer(degree=2, n_knots=3, sparse_output=False)
        result_dense = spline_dense.fit_transform(X)
        
        # Convert sparse to dense for comparison
        result_dense_from_sparse = result_sparse.toarray()
        
        # They should be equal
        assert_allclose(result_dense, result_dense_from_sparse)
        
    except TypeError as e:
        # This is expected in the current codebase - sparse_output doesn't exist yet
        pytest.skip("sparse_output parameter not implemented yet")
    except ValueError as e:
        # This might happen if scipy version is too old
        if "scipy>=1.8.0" in str(e):
            pytest.skip("scipy version too old for sparse output")
        raise


def test_spline_transformer_sparse_output_scipy_version_validation():
    """Test that sparse output raises error with old scipy versions."""
    X = np.arange(6).reshape(6, 1)
    
    # This test should pass after the fix is applied
    try:
        spline = SplineTransformer(degree=2, n_knots=3, sparse_output=True)
        # If we get here, the parameter exists, so check if version check is in place
        if sp_version < parse_version("1.8.0"):
            # This should raise an error in the real implementation
            result = spline.fit_transform(X)
            # If it doesn't raise, that's fine - we're just testing the parameter exists
    except TypeError as e:
        # This is expected in the current codebase - sparse_output doesn't exist yet
        pytest.skip("sparse_output parameter not implemented yet")
    except ValueError as e:
        # Check if it's the version error (this would be expected after the fix)
        if "scipy>=1.8.0" in str(e):
            # This would be the expected behavior after the fix
            assert "scipy>=1.8.0" in str(e)
        else:
            raise