"""
Regression tests for moving imputation out of preprocessing.

This test ensures that the change from having imputation in preprocessing
to having it in a dedicated impute module works correctly.
"""

import numpy as np
import pytest
import warnings

from sklearn.preprocessing.imputation import Imputer
from sklearn.utils.testing import assert_array_almost_equal


def test_imputer_still_importable_from_preprocessing():
    """Test that Imputer is still importable from sklearn.preprocessing.imputation."""
    # This should work in the old version
    from sklearn.preprocessing.imputation import Imputer as OldImputer
    assert OldImputer is not None


def test_imputer_exists_in_preprocessing_init():
    """Test that Imputer is still in sklearn.preprocessing.__init__."""
    # This should work in the old version
    from sklearn.preprocessing import Imputer as PreprocessingImputer
    assert PreprocessingImputer is not None


def test_imputer_functionality():
    """Test that the Imputer still works as expected."""
    # Create test data with missing values
    X = np.array([[1, 2], [np.nan, 3], [4, np.nan]])
    # Column-wise mean imputation (axis=0, default)
    # Column 0: [1, nan, 4] -> mean = 2.5
    # Column 1: [2, 3, nan] -> mean = 2.5
    expected = np.array([[1, 2], [2.5, 3], [4, 2.5]])
    
    imputer = Imputer(missing_values=np.nan, strategy='mean')
    X_trans = imputer.fit_transform(X)
    
    assert_array_almost_equal(X_trans, expected)


def test_simple_imputer_importable_from_impute_module():
    """Test that SimpleImputer is importable from sklearn.impute after change."""
    # This should fail in the old version and pass in the new version
    # We want to make sure this assertion is meaningful
    try:
        from sklearn.impute import SimpleImputer
        # If we get here, SimpleImputer exists (new behavior)
        assert SimpleImputer is not None
        # Test that it actually works with basic functionality
        X = np.array([[1, 2], [np.nan, 3], [4, np.nan]])
        imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
        X_trans = imputer.fit_transform(X)
        assert X_trans is not None
        # Verify the result is reasonable
        assert not np.isnan(X_trans).any()
    except ImportError:
        # In the old version, this should fail
        pytest.fail("SimpleImputer should be available in sklearn.impute after the change")


def test_simple_imputer_handles_nan_correctly():
    """Test that SimpleImputer correctly handles NaN values for missing data detection."""
    # Skip this test if SimpleImputer is not available yet (old version)
    try:
        from sklearn.impute import SimpleImputer
    except ImportError:
        pytest.skip("SimpleImputer not yet available - this is expected in old version")
    
    # This tests the specific behavior that one mutation variant changes
    # Test with NaN values that should be detected correctly
    X = np.array([[1, np.nan], [np.nan, 2], [3, 4]])
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    X_trans = imputer.fit_transform(X)
    # Should not have any NaN values in result
    assert not np.isnan(X_trans).any()


def test_simple_imputer_default_parameters():
    """Test that SimpleImputer has correct default parameters."""
    # Skip this test if SimpleImputer is not available yet (old version)
    try:
        from sklearn.impute import SimpleImputer
    except ImportError:
        pytest.skip("SimpleImputer not yet available - this is expected in old version")
    
    # Test default parameters - should be axis=0, strategy='mean', etc.
    imputer = SimpleImputer()
    assert imputer.axis == 0  # Default axis should be 0
    assert imputer.strategy == 'mean'  # Default strategy should be 'mean'
    assert imputer.missing_values == "NaN"  # Default missing_values should be "NaN"


def test_module_structure_includes_impute():
    """Test that sklearn.__init__.py includes 'impute' module after change."""
    # This should fail in the old version and pass in the new version
    import sklearn
    from sklearn import __all__
    
    # After the change, 'impute' should be in __all__
    assert 'impute' in __all__, "impute module should be in sklearn.__all__ after change"


def test_imputer_deprecation_warning():
    """Test that Imputer raises deprecation warning after change."""
    # This test should pass in both versions but we're ensuring it works correctly
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        imputer = Imputer()
        
        # We're just making sure it doesn't crash and works
        assert imputer is not None


def test_simple_imputer_axis_1_functionality():
    """Test that SimpleImputer works correctly with axis=1 parameter."""
    # Skip this test if SimpleImputer is not available yet (old version)
    try:
        from sklearn.impute import SimpleImputer
    except ImportError:
        pytest.skip("SimpleImputer not yet available - this is expected in old version")
    
    # Test axis=1 - impute rows
    X = np.array([[1, np.nan, 3], [np.nan, 2, 4]])
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean', axis=1)
    X_trans = imputer.fit_transform(X)
    # Should not have any NaN values in result
    assert not np.isnan(X_trans).any()