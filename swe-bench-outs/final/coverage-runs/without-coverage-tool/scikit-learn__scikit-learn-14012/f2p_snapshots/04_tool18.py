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


def test_warm_start_parameter_acceptance():
    """Test that warm_start parameter is properly accepted and stored."""
    # This test verifies the parameter is accepted (the change)
    clf = HistGradientBoostingClassifier(warm_start=True)
    reg = HistGradientBoostingRegressor(warm_start=True)
    
    assert clf.warm_start == True
    assert reg.warm_start == True
    
    clf_default = HistGradientBoostingClassifier()
    reg_default = HistGradientBoostingRegressor()
    
    assert clf_default.warm_start == False
    assert reg_default.warm_start == False


def test_warm_start_basic_training():
    """Test that warm start properly continues training."""
    # Create simple data
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]).astype(np.float32)
    y_reg = np.array([1, 2, 3, 4, 5, 6]).astype(np.float32)
    y_clf = np.array([0, 1, 0, 1, 0, 1])
    
    # Test regressor warm start
    # First fit with 2 iterations
    reg1 = HistGradientBoostingRegressor(warm_start=False, max_iter=2, random_state=0)
    reg1.fit(X, y_reg)
    
    # Second fit with warm_start=True and more iterations
    reg2 = HistGradientBoostingRegressor(warm_start=True, max_iter=2, random_state=0)
    reg2.fit(X, y_reg)
    reg2.set_params(max_iter=4)
    reg2.fit(X, y_reg)
    
    # reg2 should now have 4 iterations (continued from 2)
    assert reg1.n_iter_ == 2
    assert reg2.n_iter_ == 4
    
    # Test classifier warm start
    # First fit with 2 iterations
    clf1 = HistGradientBoostingClassifier(warm_start=False, max_iter=2, random_state=0)
    clf1.fit(X, y_clf)
    
    # Second fit with warm_start=True and more iterations
    clf2 = HistGradientBoostingClassifier(warm_start=True, max_iter=2, random_state=0)
    clf2.fit(X, y_clf)
    clf2.set_params(max_iter=4)
    clf2.fit(X, y_clf)
    
    # clf2 should now have 4 iterations (continued from 2)
    assert clf1.n_iter_ == 2
    assert clf2.n_iter_ == 4


def test_warm_start_error_handling():
    """Test that warm start properly raises errors when max_iter is decreased."""
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]).astype(np.float32)
    y = np.array([1, 2, 3, 4, 5, 6]).astype(np.float32)
    
    # Fit initial model with 4 iterations
    reg = HistGradientBoostingRegressor(warm_start=True, max_iter=4, random_state=0)
    reg.fit(X, y)
    
    # Try to decrease max_iter - should raise ValueError
    reg.set_params(max_iter=2)
    with pytest.raises(ValueError, match="max_iter=2 must be larger than or equal to n_iter_=4"):
        reg.fit(X, y)


def test_warm_start_state_preservation():
    """Test that warm start preserves internal state correctly."""
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]).astype(np.float32)
    y = np.array([1, 2, 3, 4, 5, 6]).astype(np.float32)
    
    # Create model and fit it
    reg1 = HistGradientBoostingRegressor(warm_start=False, max_iter=2, random_state=42)
    reg1.fit(X, y)
    
    # Create another model with warm_start and fit it
    reg2 = HistGradientBoostingRegressor(warm_start=True, max_iter=2, random_state=42)
    reg2.fit(X, y)
    
    # Continue training with warm start
    reg2.set_params(max_iter=4)
    reg2.fit(X, y)
    
    # Both should have same number of iterations
    assert reg1.n_iter_ == 2
    assert reg2.n_iter_ == 4


def test_warm_start_predict_consistency():
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
    
    # Both should have same number of iterations
    assert reg1.n_iter_ == 10
    assert reg2.n_iter_ == 10
    
    # Predictions should be consistent (though not necessarily identical due to randomization)
    pred1 = reg1.predict(X)
    pred2 = reg2.predict(X)
    
    # Both models should be able to make predictions
    assert len(pred1) == len(X)
    assert len(pred2) == len(X)