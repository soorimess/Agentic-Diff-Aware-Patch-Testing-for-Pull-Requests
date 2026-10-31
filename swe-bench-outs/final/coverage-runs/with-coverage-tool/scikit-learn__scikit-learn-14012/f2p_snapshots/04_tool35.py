"""
Test for warm start functionality in histogram-based GBM.

This test verifies that the warm_start parameter works correctly in
HistGradientBoostingClassifier and HistGradientBoostingRegressor.
"""
import numpy as np
import pytest
from sklearn.datasets import make_classification, make_regression
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier


def test_warm_start_basic_functionality():
    """Test that warm_start parameter is accepted and works correctly."""
    # Generate simple data
    X, y = make_regression(n_samples=100, n_features=5, noise=0.1, random_state=42)
    
    # First fit with warm_start=True
    gb = HistGradientBoostingRegressor(warm_start=True, max_iter=30, random_state=42)
    gb.fit(X, y)
    
    # Store initial state
    initial_n_iter = gb.n_iter_
    
    # Second fit with more iterations - should continue from previous fit
    gb.set_params(max_iter=60)
    gb.fit(X, y)
    
    # Should have more iterations
    assert gb.n_iter_ == 60
    assert initial_n_iter < gb.n_iter_


def test_warm_start_error_when_max_iter_smaller():
    """Test that warm start raises error when max_iter is smaller than previous n_iter."""
    # Generate simple data
    X, y = make_regression(n_samples=100, n_features=5, noise=0.1, random_state=42)
    
    # First fit
    gb = HistGradientBoostingRegressor(warm_start=True, max_iter=50, random_state=42)
    gb.fit(X, y)
    
    # Try to fit again with smaller max_iter - should raise ValueError
    gb.set_params(max_iter=20)
    with pytest.raises(ValueError, match="max_iter=20 must be larger than or equal to n_iter_=50"):
        gb.fit(X, y)


def test_warm_start_consistent_predictions():
    """Test that warm start produces consistent predictions."""
    # Generate simple data
    X, y = make_regression(n_samples=100, n_features=5, noise=0.1, random_state=42)
    
    # First fit
    gb1 = HistGradientBoostingRegressor(warm_start=True, max_iter=30, random_state=42)
    gb1.fit(X, y)
    
    # Second fit with more iterations
    gb1.set_params(max_iter=60)
    gb1.fit(X, y)
    
    # Predictions should be consistent
    pred1 = gb1.predict(X)
    
    # Create a new model and fit it in one go
    gb2 = HistGradientBoostingRegressor(warm_start=False, max_iter=60, random_state=42)
    gb2.fit(X, y)
    pred2 = gb2.predict(X)
    
    # The predictions should be the same (or very close)
    np.testing.assert_allclose(pred1, pred2, rtol=1e-10)


def test_warm_start_classifier():
    """Test warm start with classifier."""
    # Generate simple data
    X, y = make_classification(n_samples=100, n_features=5, n_classes=2, 
                              n_informative=3, random_state=42)
    
    # First fit
    gb = HistGradientBoostingClassifier(warm_start=True, max_iter=30, random_state=42)
    gb.fit(X, y)
    
    # Store initial state
    initial_n_iter = gb.n_iter_
    
    # Second fit with more iterations
    gb.set_params(max_iter=60)
    gb.fit(X, y)
    
    # Should have more iterations
    assert gb.n_iter_ == 60
    assert initial_n_iter < gb.n_iter_


def test_warm_start_with_validation_data():
    """Test warm start with validation data."""
    # Generate simple data
    X, y = make_classification(n_samples=100, n_features=5, n_classes=2, 
                              n_informative=3, random_state=42)
    
    # First fit with validation data
    gb = HistGradientBoostingClassifier(warm_start=True, max_iter=30, 
                                       validation_fraction=0.2, random_state=42)
    gb.fit(X, y)
    
    # Store initial state
    initial_n_iter = gb.n_iter_
    
    # Second fit with more iterations
    gb.set_params(max_iter=60)
    gb.fit(X, y)
    
    # Should have more iterations
    assert gb.n_iter_ == 60
    assert initial_n_iter < gb.n_iter_


def test_warm_start_without_validation_data():
    """Test warm start when no validation data is used (validation_fraction=None)."""
    # Generate simple data
    X, y = make_regression(n_samples=100, n_features=5, noise=0.1, random_state=42)
    
    # First fit without validation data (set to None)
    gb = HistGradientBoostingRegressor(warm_start=True, max_iter=30, 
                                      validation_fraction=None, random_state=42)
    gb.fit(X, y)
    
    # Store initial state
    initial_n_iter = gb.n_iter_
    
    # Second fit with more iterations
    gb.set_params(max_iter=60)
    gb.fit(X, y)
    
    # Should have more iterations
    assert gb.n_iter_ == 60
    assert initial_n_iter < gb.n_iter_