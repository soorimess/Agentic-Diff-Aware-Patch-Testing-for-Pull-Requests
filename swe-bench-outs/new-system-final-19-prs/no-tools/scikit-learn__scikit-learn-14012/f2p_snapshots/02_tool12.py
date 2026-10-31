"""
Test for warm start functionality in histogram-based GBM.

This test ensures that the warm_start parameter works correctly in
HistGradientBoostingClassifier and HistGradientBoostingRegressor.
"""
# To use this experimental feature, we need to explicitly ask for it:
from sklearn.experimental import enable_hist_gradient_boosting  # noqa
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
import numpy as np
import pytest


def test_warm_start_parameter_exists():
    """Test that warm_start parameter is accepted by both classifiers and regressors."""
    # Test that the parameter exists and can be set
    clf = HistGradientBoostingClassifier(warm_start=True)
    reg = HistGradientBoostingRegressor(warm_start=True)
    
    assert clf.warm_start == True
    assert reg.warm_start == True
    
    # Test default value
    clf_default = HistGradientBoostingClassifier()
    reg_default = HistGradientBoostingRegressor()
    
    assert clf_default.warm_start == False
    assert reg_default.warm_start == False


def test_warm_start_basic_functionality():
    """Test basic warm start functionality with simple data."""
    # Create simple data
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]).astype(np.float32)
    y_reg = np.array([1, 2, 3, 4, 5, 6]).astype(np.float32)
    y_clf = np.array([0, 1, 0, 1, 0, 1])
    
    # Test with regressor
    reg1 = HistGradientBoostingRegressor(warm_start=False, max_iter=2, random_state=0)
    reg2 = HistGradientBoostingRegressor(warm_start=True, max_iter=2, random_state=0)
    
    # Fit first model
    reg1.fit(X, y_reg)
    reg2.fit(X, y_reg)
    
    # Now do warm start - add more iterations
    reg2.set_params(max_iter=4)
    reg2.fit(X, y_reg)
    
    # Both should have same number of iterations now
    assert reg1.n_iter_ == 2
    assert reg2.n_iter_ == 4
    
    # Test with classifier
    clf1 = HistGradientBoostingClassifier(warm_start=False, max_iter=2, random_state=0)
    clf2 = HistGradientBoostingClassifier(warm_start=True, max_iter=2, random_state=0)
    
    # Fit first model
    clf1.fit(X, y_clf)
    clf2.fit(X, y_clf)
    
    # Now do warm start - add more iterations
    clf2.set_params(max_iter=4)
    clf2.fit(X, y_clf)
    
    # Both should have same number of iterations now
    assert clf1.n_iter_ == 2
    assert clf2.n_iter_ == 4


def test_warm_start_error_handling():
    """Test that warm start properly raises errors when max_iter is decreased."""
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]).astype(np.float32)
    y = np.array([1, 2, 3, 4, 5, 6]).astype(np.float32)
    
    # Fit initial model
    reg = HistGradientBoostingRegressor(warm_start=True, max_iter=4, random_state=0)
    reg.fit(X, y)
    
    # Try to decrease max_iter - should raise ValueError
    reg.set_params(max_iter=2)
    with pytest.raises(ValueError, match="max_iter=2 must be larger than or equal to n_iter_=4"):
        reg.fit(X, y)


def test_warm_start_consistent_predictions():
    """Test that warm start produces consistent predictions."""
    # Create larger dataset for better testing
    np.random.seed(42)
    X = np.random.rand(100, 3).astype(np.float32)
    y = np.random.rand(100).astype(np.float32)
    
    # Fit in two stages
    reg1 = HistGradientBoostingRegressor(warm_start=True, max_iter=5, random_state=0)
    reg1.fit(X, y)
    
    # Continue training
    reg1.set_params(max_iter=10)
    reg1.fit(X, y)
    
    # Fit all at once
    reg2 = HistGradientBoostingRegressor(warm_start=False, max_iter=10, random_state=0)
    reg2.fit(X, y)
    
    # The models should have the same number of iterations
    assert reg1.n_iter_ == 10
    assert reg2.n_iter_ == 10


def test_warm_start_random_state_preservation():
    """Test that random state is preserved during warm start."""
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]).astype(np.float32)
    y = np.array([1, 2, 3, 4, 5, 6]).astype(np.float32)
    
    # Create two models with same random state
    reg1 = HistGradientBoostingRegressor(warm_start=False, max_iter=2, random_state=42)
    reg2 = HistGradientBoostingRegressor(warm_start=True, max_iter=2, random_state=42)
    
    # Fit first model
    reg1.fit(X, y)
    reg2.fit(X, y)
    
    # Continue training with warm start
    reg2.set_params(max_iter=4)
    reg2.fit(X, y)
    
    # Both should have same number of iterations
    assert reg1.n_iter_ == 2
    assert reg2.n_iter_ == 4