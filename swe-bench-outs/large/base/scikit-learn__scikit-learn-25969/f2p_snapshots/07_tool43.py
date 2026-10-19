"""
Regression tests for PR that adds CurveDisplayMixin _get_response_values.

This test ensures that the new _BinaryClassifierCurveDisplayMixin functionality
works correctly and that the refactored plotting classes behave as expected.
"""

import numpy as np
import pytest
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibrationDisplay


def test_new_validation_methods_exist():
    """Test that the new validation methods exist on CalibrationDisplay."""
    # This test will fail in the current version but pass after the PR is applied
    # It specifically tests the key behavioral change: new validation methods exist
    assert hasattr(CalibrationDisplay, '_validate_and_get_response_values')
    assert hasattr(CalibrationDisplay, '_validate_from_predictions_params')
    assert hasattr(CalibrationDisplay, '_validate_plot_params')


def test_calibration_display_parameter_handling():
    """Test that CalibrationDisplay properly handles parameters in new validation flow."""
    # Create test data
    X, y = make_classification(n_samples=50, n_features=10, n_classes=2, 
                              n_informative=5, random_state=42)
    
    # Create and fit a classifier
    clf = LogisticRegression(random_state=42)
    clf.fit(X, y)
    
    # Test from_estimator with proper parameter validation
    # This should properly pass all parameters to the new validation method
    disp = CalibrationDisplay.from_estimator(
        clf, X, y, name="Test Classifier", pos_label=1
    )
    
    # Basic functionality checks
    assert hasattr(disp, 'line_')
    assert hasattr(disp, 'ax_')
    assert hasattr(disp, 'figure_')
    assert disp.estimator_name == "Test Classifier"
    
    # Test from_predictions with proper parameter validation
    y_prob = clf.predict_proba(X)[:, 1]
    disp2 = CalibrationDisplay.from_predictions(
        y, y_prob, name="Test Classifier 2", pos_label=1
    )
    
    assert hasattr(disp2, 'line_')
    assert hasattr(disp2, 'ax_')
    assert hasattr(disp2, 'figure_')
    assert disp2.estimator_name == "Test Classifier 2"


def test_calibration_display_plot_validation():
    """Test that CalibrationDisplay plot method works with new validation."""
    # Create a simple CalibrationDisplay instance
    prob_true = np.array([0.0, 0.5, 1.0])
    prob_pred = np.array([0.0, 0.5, 1.0])
    y_prob = np.array([0.0, 0.5, 1.0])
    
    disp = CalibrationDisplay(
        prob_true=prob_true,
        prob_pred=prob_pred,
        y_prob=y_prob,
        estimator_name="Test"
    )
    
    # This should work and use the new validation approach
    result = disp.plot()
    assert hasattr(result, 'line_')
    assert hasattr(result, 'ax_')
    assert hasattr(result, 'figure_')
    
    # Check that the plot method properly sets up the axes
    assert result.ax_ is not None
    assert result.figure_ is not None


def test_pos_label_validation():
    """Test that pos_label validation works correctly with new validation methods."""
    # Test with {-1, 1} labels (should infer pos_label=1)
    y_true = np.array([-1, -1, 1, 1])
    y_prob = np.array([0.1, 0.4, 0.6, 0.9])
    
    # This should work and infer pos_label=1 properly
    disp = CalibrationDisplay.from_predictions(y_true, y_prob)
    assert hasattr(disp, 'line_')
    assert hasattr(disp, 'ax_')
    assert hasattr(disp, 'figure_')
    
    # Test with 0, 1 labels
    y_true_01 = np.array([0, 0, 1, 1])
    disp2 = CalibrationDisplay.from_predictions(y_true_01, y_prob)
    assert hasattr(disp2, 'line_')
    assert hasattr(disp2, 'ax_')
    assert hasattr(disp2, 'figure_')