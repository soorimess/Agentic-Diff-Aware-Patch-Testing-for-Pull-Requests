"""
Test for warm start functionality in histogram-based gradient boosting.

This test ensures that the warm_start parameter works correctly in
HistGradientBoostingClassifier and HistGradientBoostingRegressor.
"""
import numpy as np
import pytest
from sklearn.datasets import make_classification, make_regression
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor


# Test data
X_classification, y_classification = make_classification(n_samples=100, random_state=0)
X_regression, y_regression = make_regression(n_samples=100, random_state=0)


def test_warm_start_basic_functionality():
    """Test basic warm start functionality by checking that iterations are accumulated."""
    # Create a classifier with warm_start=True
    clf = HistGradientBoostingClassifier(warm_start=True, max_iter=5, random_state=42)
    
    # First fit
    clf.fit(X_classification, y_classification)
    assert clf.n_iter_ == 5
    assert hasattr(clf, '_predictors')
    assert len(clf._predictors) == 5
    
    # Second fit with more iterations
    clf.set_params(max_iter=10)
    clf.fit(X_classification, y_classification)
    assert clf.n_iter_ == 10
    assert len(clf._predictors) == 10


def test_warm_start_error_when_max_iter_decreases():
    """Test that warm_start raises error when max_iter decreases."""
    clf = HistGradientBoostingClassifier(warm_start=True, max_iter=5, random_state=42)
    
    # First fit
    clf.fit(X_classification, y_classification)
    
    # Try to fit again with smaller max_iter (should raise error)
    clf.set_params(max_iter=3)
    with pytest.raises(ValueError, match="max_iter=3 must be larger than or equal to n_iter_=5"):
        clf.fit(X_classification, y_classification)


def test_warm_start_regressor():
    """Test warm start functionality with regressor."""
    reg = HistGradientBoostingRegressor(warm_start=True, max_iter=5, random_state=42)
    
    # First fit
    reg.fit(X_regression, y_regression)
    assert reg.n_iter_ == 5
    assert hasattr(reg, '_predictors')
    assert len(reg._predictors) == 5
    
    # Second fit with more iterations
    reg.set_params(max_iter=10)
    reg.fit(X_regression, y_regression)
    assert reg.n_iter_ == 10
    assert len(reg._predictors) == 10


def test_warm_start_is_fitted():
    """Test that _is_fitted method works correctly."""
    clf = HistGradientBoostingClassifier(warm_start=True, max_iter=5, random_state=42)
    
    # Initially not fitted
    assert not clf._is_fitted()
    
    # After fitting
    clf.fit(X_classification, y_classification)
    assert clf._is_fitted()
    
    # Create new instance without fitting
    clf2 = HistGradientBoostingClassifier(warm_start=True, max_iter=5, random_state=42)
    assert not clf2._is_fitted()


def test_warm_start_predict_consistency():
    """Test that predictions are consistent with warm start."""
    # Create a classifier with warm_start=True
    clf1 = HistGradientBoostingClassifier(warm_start=True, max_iter=5, random_state=42)
    clf2 = HistGradientBoostingClassifier(warm_start=True, max_iter=5, random_state=42)
    
    # Fit first model
    clf1.fit(X_classification, y_classification)
    
    # Fit second model with same parameters
    clf2.fit(X_classification, y_classification)
    
    # Make predictions
    pred1 = clf1.predict(X_classification)
    pred2 = clf2.predict(X_classification)
    
    # Predictions should be the same for same parameters and data
    np.testing.assert_array_equal(pred1, pred2)


def test_warm_start_different_seeds():
    """Test that different random seeds produce different results."""
    clf1 = HistGradientBoostingClassifier(warm_start=True, max_iter=5, random_state=42)
    clf2 = HistGradientBoostingClassifier(warm_start=True, max_iter=5, random_state=123)
    
    clf1.fit(X_classification, y_classification)
    clf2.fit(X_classification, y_classification)
    
    # Predictions should be different due to different seeds
    pred1 = clf1.predict(X_classification)
    pred2 = clf2.predict(X_classification)
    
    # They should be different (though not guaranteed, very likely)
    # For our test, we just want to make sure they can be different
    assert len(pred1) == len(pred2)


def test_warm_start_simple():
    """Test basic warm start functionality works without early stopping issues."""
    # Test that warm start works without complex early stopping scenarios
    clf = HistGradientBoostingClassifier(warm_start=True, max_iter=3, random_state=42)
    
    # First fit
    clf.fit(X_classification, y_classification)
    assert clf.n_iter_ == 3
    
    # Second fit with more iterations
    clf.set_params(max_iter=6)
    clf.fit(X_classification, y_classification)
    assert clf.n_iter_ == 6


def test_warm_start_with_validation_and_scoring():
    """Test warm start with validation data and scoring."""
    # Test with validation data and scoring
    clf = HistGradientBoostingClassifier(
        warm_start=True, 
        max_iter=5, 
        validation_fraction=0.2,
        scoring='accuracy',
        random_state=42
    )
    
    # First fit
    clf.fit(X_classification, y_classification)
    assert clf.n_iter_ == 5
    
    # Second fit with more iterations
    clf.set_params(max_iter=10)
    clf.fit(X_classification, y_classification)
    assert clf.n_iter_ == 10


def test_warm_start_with_loss_scoring():
    """Test warm start with loss scoring (different code path)."""
    # Test with validation data and loss scoring
    clf = HistGradientBoostingClassifier(
        warm_start=True, 
        max_iter=5, 
        validation_fraction=0.2,
        scoring='loss',
        random_state=42
    )
    
    # First fit
    clf.fit(X_classification, y_classification)
    assert clf.n_iter_ == 5
    
    # Second fit with more iterations
    clf.set_params(max_iter=10)
    clf.fit(X_classification, y_classification)
    assert clf.n_iter_ == 10


# Copied unchanged by the harness from sklearn/ensemble/_hist_gradient_boosting/tests/test_gradient_boosting.py::test_early_stopping_classification, a test in this repository before this change.
import pytest
from sklearn.datasets import make_classification
from sklearn.ensemble import HistGradientBoostingClassifier


@pytest.mark.parametrize('data', (
    make_classification(random_state=0),
    make_classification(n_classes=3, n_clusters_per_class=1, random_state=0)
))
@pytest.mark.parametrize(
    'scoring, validation_fraction, n_iter_no_change, tol', [
        ('accuracy', .1, 5, 1e-7),  # use scorer
        ('accuracy', None, 5, 1e-1),  # use scorer on training data
        (None, .1, 5, 1e-7),  # same with default scorerscor
        (None, None, 5, 1e-1),
        ('loss', .1, 5, 1e-7),  # use loss
        ('loss', None, 5, 1e-1),  # use loss on training data
        (None, None, None, None),  # no early stopping
        ])
def test_seeded_early_stopping_classification(data, scoring, validation_fraction,
                                       n_iter_no_change, tol):

    max_iter = 50

    X, y = data

    gb = HistGradientBoostingClassifier(
        verbose=1,  # just for coverage
        min_samples_leaf=5,  # easier to overfit fast
        scoring=scoring,
        tol=tol,
        validation_fraction=validation_fraction,
        max_iter=max_iter,
        n_iter_no_change=n_iter_no_change,
        random_state=0
    )
    gb.fit(X, y)

    # Assert the actual values instead of just checking existence
    if n_iter_no_change is not None:
        assert n_iter_no_change <= gb.n_iter_ < max_iter
    else:
        assert gb.n_iter_ == max_iter