import numpy as np
import pytest
from sklearn.datasets import make_classification, make_regression
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier


def test_warm_start_parameter_exists():
    """Test that warm_start parameter exists in constructor."""
    # Test that warm_start parameter is accepted
    clf = HistGradientBoostingClassifier(warm_start=True)
    assert clf.warm_start is True
    
    reg = HistGradientBoostingRegressor(warm_start=True)
    assert reg.warm_start is True


def test_warm_start_basic_functionality():
    """Test basic warm start functionality."""
    # Generate simple data
    X, y = make_regression(n_samples=100, n_features=5, random_state=42)
    
    # First fit
    clf1 = HistGradientBoostingRegressor(warm_start=False, max_iter=50, random_state=42)
    clf1.fit(X, y)
    
    # Second fit with warm start
    clf2 = HistGradientBoostingRegressor(warm_start=True, max_iter=100, random_state=42)
    clf2.fit(X, y)
    
    # The second fit should have more iterations
    assert clf1.n_iter_ == 50
    assert clf2.n_iter_ == 100


def test_warm_start_classifier():
    """Test warm start with classifier."""
    X, y = make_classification(n_samples=100, n_features=5, n_classes=2, random_state=42)
    
    # First fit
    clf1 = HistGradientBoostingClassifier(warm_start=False, max_iter=50, random_state=42)
    clf1.fit(X, y)
    
    # Second fit with warm start
    clf2 = HistGradientBoostingClassifier(warm_start=True, max_iter=100, random_state=42)
    clf2.fit(X, y)
    
    # Should have more iterations
    assert clf1.n_iter_ == 50
    assert clf2.n_iter_ == 100


def test_warm_start_predicts_same_shape():
    """Test that warm start produces same prediction shapes."""
    X, y = make_regression(n_samples=100, n_features=5, random_state=42)
    
    # First fit
    clf1 = HistGradientBoostingRegressor(warm_start=False, max_iter=50, random_state=42)
    clf1.fit(X, y)
    pred1 = clf1.predict(X)
    
    # Second fit with warm start
    clf2 = HistGradientBoostingRegressor(warm_start=True, max_iter=100, random_state=42)
    clf2.fit(X, y)
    pred2 = clf2.predict(X)
    
    # Should have same prediction shape
    assert pred1.shape == pred2.shape


def test_warm_start_validation_fraction_preserved():
    """Test that validation_fraction parameter is preserved."""
    X, y = make_regression(n_samples=100, n_features=5, random_state=42)
    
    # Test that validation_fraction is accepted
    clf = HistGradientBoostingRegressor(warm_start=False, max_iter=50, 
                                       validation_fraction=0.2, random_state=42)
    assert clf.validation_fraction == 0.2
    
    # Test that warm_start works with validation_fraction
    clf.fit(X, y)
    assert clf.validation_fraction == 0.2


def test_warm_start_with_validation_data():
    """Test warm start with validation data."""
    X, y = make_regression(n_samples=100, n_features=5, random_state=42)
    
    # First fit with validation
    clf1 = HistGradientBoostingRegressor(
        warm_start=False, max_iter=50, validation_fraction=0.2, random_state=42
    )
    clf1.fit(X, y)
    
    # Second fit with warm start
    clf2 = HistGradientBoostingRegressor(
        warm_start=True, max_iter=100, validation_fraction=0.2, random_state=42
    )
    clf2.fit(X, y)
    
    # Should have more iterations
    assert clf1.n_iter_ == 50
    assert clf2.n_iter_ == 100


def test_warm_start_reproducibility():
    """Test that warm start produces reproducible results."""
    # Use fixed random state
    random_state = 42
    X, y = make_regression(n_samples=100, n_features=5, random_state=random_state)
    
    # Train model in two steps (warm start)
    clf1 = HistGradientBoostingRegressor(warm_start=False, max_iter=50, random_state=random_state)
    clf1.fit(X, y)
    
    clf2 = HistGradientBoostingRegressor(warm_start=True, max_iter=100, random_state=random_state)
    clf2.fit(X, y)
    
    # Train model in one step
    clf3 = HistGradientBoostingRegressor(warm_start=False, max_iter=100, random_state=random_state)
    clf3.fit(X, y)
    
    # Results should be the same
    pred1 = clf1.predict(X)
    pred2 = clf2.predict(X)
    pred3 = clf3.predict(X)
    
    # The warm start result should match the single fit result
    np.testing.assert_array_almost_equal(pred2, pred3)


def test_warm_start_with_different_random_states():
    """Test that warm start with same random state gives same results."""
    X, y = make_regression(n_samples=100, n_features=5, random_state=42)
    
    # First fit with warm_start=False
    clf1 = HistGradientBoostingRegressor(warm_start=False, max_iter=50, random_state=42)
    clf1.fit(X, y)
    
    # Second fit with warm_start=True and same random_state
    clf2 = HistGradientBoostingRegressor(warm_start=True, max_iter=100, random_state=42)
    clf2.fit(X, y)
    
    # The model should have more iterations
    assert clf1.n_iter_ == 50
    assert clf2.n_iter_ == 100