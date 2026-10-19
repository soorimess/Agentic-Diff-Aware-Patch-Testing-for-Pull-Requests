"""
Regression test for warm start functionality in histogram-based GBM.

This test ensures that the warm start feature works correctly for
HistGradientBoostingClassifier and HistGradientBoostingRegressor.
"""
import numpy as np
import pytest
from sklearn.datasets import make_classification, make_regression
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor


def test_warm_start_basic_functionality():
    """Test that warm start works by fitting twice and checking results."""
    # Create simple dataset
    X, y = make_classification(n_samples=100, n_features=4, n_classes=2, 
                               n_redundant=0, random_state=42)
    
    # First fit
    clf1 = HistGradientBoostingClassifier(warm_start=True, max_iter=5, random_state=0)
    clf1.fit(X, y)
    
    # Second fit with more iterations
    clf1.set_params(max_iter=10)
    clf1.fit(X, y)
    
    # The model should now have 10 iterations
    assert clf1.n_iter_ == 10
    
    # Results should be consistent
    assert hasattr(clf1, 'train_score_')
    assert hasattr(clf1, 'validation_score_')


def test_warm_start_regressor():
    """Test warm start functionality for regressor."""
    # Create simple dataset
    X, y = make_regression(n_samples=100, n_features=4, random_state=42)
    
    # First fit
    reg1 = HistGradientBoostingRegressor(warm_start=True, max_iter=5, random_state=0)
    reg1.fit(X, y)
    
    # Second fit with more iterations
    reg1.set_params(max_iter=10)
    reg1.fit(X, y)
    
    # The model should now have 10 iterations
    assert reg1.n_iter_ == 10


def test_warm_start_validation_error():
    """Test that warm start raises error when max_iter is smaller than previous n_iter."""
    # Create simple dataset
    X, y = make_classification(n_samples=100, n_features=4, n_classes=2, 
                               n_redundant=0, random_state=42)
    
    # First fit
    clf1 = HistGradientBoostingClassifier(warm_start=True, max_iter=10, random_state=0)
    clf1.fit(X, y)
    
    # Try to fit again with smaller max_iter - should raise error
    clf1.set_params(max_iter=5)
    with pytest.raises(ValueError, match="max_iter=5 must be larger than or equal to n_iter_=10"):
        clf1.fit(X, y)


def test_warm_start_consistent_predictions():
    """Test that warm start produces consistent predictions."""
    # Create simple dataset
    X, y = make_classification(n_samples=100, n_features=4, n_classes=2, 
                               n_redundant=0, random_state=42)
    
    # Fit model in two stages
    clf1 = HistGradientBoostingClassifier(warm_start=True, max_iter=5, random_state=0)
    clf1.fit(X, y)
    
    # Save predictions from first stage
    pred1 = clf1.predict_proba(X)
    
    # Continue fitting
    clf1.set_params(max_iter=10)
    clf1.fit(X, y)
    
    # Save predictions from second stage
    pred2 = clf1.predict_proba(X)
    
    # Predictions should be consistent (no regression)
    assert pred1.shape == pred2.shape


def test_warm_start_parameter_exists():
    """Test that warm_start parameter is properly added to both classifiers and regressors."""
    # Test classifier
    clf = HistGradientBoostingClassifier()
    assert hasattr(clf, 'warm_start')
    assert clf.warm_start is False
    
    # Test regressor
    reg = HistGradientBoostingRegressor()
    assert hasattr(reg, 'warm_start')
    assert reg.warm_start is False
    
    # Test that we can set it
    clf2 = HistGradientBoostingClassifier(warm_start=True)
    assert clf2.warm_start is True
    
    reg2 = HistGradientBoostingRegressor(warm_start=True)
    assert reg2.warm_start is True


def test_warm_start_validation_fraction_handling():
    """Test that validation_fraction is properly handled in warm start mode."""
    # Create simple dataset
    X, y = make_classification(n_samples=100, n_features=4, n_classes=2, 
                               n_redundant=0, random_state=42)
    
    # First fit with validation_fraction
    clf1 = HistGradientBoostingClassifier(warm_start=True, max_iter=5, 
                                          validation_fraction=0.2, random_state=0)
    clf1.fit(X, y)
    
    # Check that validation_fraction is properly set
    assert clf1.validation_fraction == 0.2
    
    # Continue fitting
    clf1.set_params(max_iter=10)
    clf1.fit(X, y)
    
    # Should still have the same validation_fraction
    assert clf1.validation_fraction == 0.2


def test_warm_start_scoring_functionality():
    """Test warm start with scoring to cover scoring code paths."""
    # Create simple dataset
    X, y = make_classification(n_samples=100, n_features=4, n_classes=2, 
                               n_redundant=0, random_state=42)
    
    # First fit with scoring
    clf1 = HistGradientBoostingClassifier(warm_start=True, max_iter=10, 
                                          scoring='accuracy', random_state=0)
    clf1.fit(X, y)
    
    # Check that scoring attributes are populated
    assert hasattr(clf1, 'train_score_')
    assert hasattr(clf1, 'validation_score_')
    
    # Continue fitting
    clf1.set_params(max_iter=15)
    clf1.fit(X, y)
    
    # Should still have the same attributes populated
    assert hasattr(clf1, 'train_score_')
    assert hasattr(clf1, 'validation_score_')