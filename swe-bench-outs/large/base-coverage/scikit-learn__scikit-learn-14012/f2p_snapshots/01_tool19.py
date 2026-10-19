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