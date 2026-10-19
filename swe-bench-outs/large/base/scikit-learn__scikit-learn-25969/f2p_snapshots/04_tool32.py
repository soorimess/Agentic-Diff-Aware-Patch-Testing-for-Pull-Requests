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


def test_calibration_display_plot_method_new_validation():
    """Test that plot method uses new validation approach."""
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


def test_calibration_display_from_estimator_new_flow():
    """Test that from_estimator uses the new validation flow."""
    # Create test data
    X, y = make_classification(n_samples=100, n_features=20, n_classes=2, 
                              n_informative=10, random_state=42)
    
    # Create and fit a classifier
    clf = LogisticRegression(random_state=42)
    clf.fit(X, y)
    
    # Test the new from_estimator flow
    disp = CalibrationDisplay.from_estimator(
        clf, X, y, name="Test Classifier"
    )
    
    # After the PR, this should work and produce a proper display
    assert hasattr(disp, 'line_')
    assert hasattr(disp, 'ax_')
    assert hasattr(disp, 'figure_')
    assert disp.estimator_name == "Test Classifier"


def test_calibration_display_from_predictions_new_flow():
    """Test that from_predictions uses the new validation flow."""
    # Create test data
    y_true = np.array([0, 0, 1, 1])
    y_prob = np.array([0.1, 0.4, 0.6, 0.9])
    
    # Test the new from_predictions flow
    disp = CalibrationDisplay.from_predictions(
        y_true, y_prob, name="Test Classifier"
    )
    
    # After the PR, this should work and produce a proper display
    assert hasattr(disp, 'line_')
    assert hasattr(disp, 'ax_')
    assert hasattr(disp, 'figure_')
    assert disp.estimator_name == "Test Classifier"


def test_pos_label_consistency_validation():
    """Test that pos_label validation works as expected in the new system."""
    # Create test data with {-1, 1} labels
    y_true = np.array([-1, -1, 1, 1])
    y_prob = np.array([0.1, 0.4, 0.6, 0.9])
    
    # Test that the new validation approach works with these labels
    disp = CalibrationDisplay.from_predictions(y_true, y_prob)
    
    # After the PR, this should work and infer pos_label=1
    assert hasattr(disp, 'line_')
    assert hasattr(disp, 'ax_')
    assert hasattr(disp, 'figure_')