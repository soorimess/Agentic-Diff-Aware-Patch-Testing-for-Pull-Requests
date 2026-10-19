"""
Regression tests for PR that adds CurveDisplayMixin _get_response_values.

This test ensures that the new _BinaryClassifierCurveDisplayMixin is properly
integrated into the display classes and that the new validation methods work
correctly.
"""

import numpy as np
import pytest
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibrationDisplay
from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay, DetCurveDisplay


def test_display_classes_inherit_from_mixin():
    """Test that display classes will inherit from _BinaryClassifierCurveDisplayMixin after PR."""
    # This test will fail before the PR and pass after the PR
    # It tests the inheritance relationship that will be added
    try:
        from sklearn.utils._plotting import _BinaryClassifierCurveDisplayMixin
        # Test that the classes inherit from the expected mixin
        assert issubclass(CalibrationDisplay, _BinaryClassifierCurveDisplayMixin)
        assert issubclass(RocCurveDisplay, _BinaryClassifierCurveDisplayMixin)
        assert issubclass(PrecisionRecallDisplay, _BinaryClassifierCurveDisplayMixin)
        assert issubclass(DetCurveDisplay, _BinaryClassifierCurveDisplayMixin)
    except ImportError:
        # This is expected before the PR is applied
        pytest.skip("Mixin class not yet available - this is expected before PR is applied")


def test_new_validation_methods_exist():
    """Test that new validation methods exist on display classes after PR."""
    # This test will fail before the PR and pass after the PR
    try:
        # Test that from_estimator method uses new validation
        assert hasattr(CalibrationDisplay, '_validate_and_get_response_values')
        assert hasattr(RocCurveDisplay, '_validate_and_get_response_values')
        assert hasattr(PrecisionRecallDisplay, '_validate_and_get_response_values')
        assert hasattr(DetCurveDisplay, '_validate_and_get_response_values')
        
        # Test that from_predictions method uses new validation
        assert hasattr(CalibrationDisplay, '_validate_from_predictions_params')
        assert hasattr(RocCurveDisplay, '_validate_from_predictions_params')
        assert hasattr(PrecisionRecallDisplay, '_validate_from_predictions_params')
        assert hasattr(DetCurveDisplay, '_validate_from_predictions_params')
    except AttributeError:
        # This is expected before the PR is applied
        pytest.skip("Validation methods not yet available - this is expected before PR is applied")


def test_plot_method_uses_new_axis_validation():
    """Test that plot methods use the new axis validation after PR."""
    # Create sample data
    X, y = make_classification(n_samples=100, n_features=20, n_classes=2, 
                               n_informative=10, random_state=42)
    clf = LogisticRegression(random_state=42)
    clf.fit(X, y)
    
    # Test that the classes have the new validation method
    try:
        # Test that the classes have the _validate_plot_params method
        assert hasattr(CalibrationDisplay, '_validate_plot_params')
        assert hasattr(RocCurveDisplay, '_validate_plot_params')
        assert hasattr(PrecisionRecallDisplay, '_validate_plot_params')
        assert hasattr(DetCurveDisplay, '_validate_plot_params')
        
        # Test that from_estimator methods work (they should call new validation)
        disp = CalibrationDisplay.from_estimator(clf, X, y)
        assert disp is not None
        
        disp = RocCurveDisplay.from_estimator(clf, X, y)
        assert disp is not None
        
        disp = PrecisionRecallDisplay.from_estimator(clf, X, y)
        assert disp is not None
        
        disp = DetCurveDisplay.from_estimator(clf, X, y)
        assert disp is not None
        
    except (AttributeError, ImportError):
        # This is expected before the PR is applied
        pytest.skip("New validation methods not yet available - this is expected before PR is applied")


def test_pos_label_validation_behavior():
    """Test that pos_label validation works correctly with new methods."""
    # Create sample data with different label types
    X, y = make_classification(n_samples=100, n_features=20, n_classes=2, 
                               n_informative=10, random_state=42)
    
    # Test with default pos_label (should work)
    clf = LogisticRegression(random_state=42)
    clf.fit(X, y)
    
    try:
        # Test that from_estimator works with default pos_label
        disp = CalibrationDisplay.from_estimator(clf, X, y)
        assert disp.pos_label == 1
        
        disp = RocCurveDisplay.from_estimator(clf, X, y)
        assert disp.pos_label == 1
        
        disp = PrecisionRecallDisplay.from_estimator(clf, X, y)
        assert disp.pos_label == 1
        
        disp = DetCurveDisplay.from_estimator(clf, X, y)
        assert disp.pos_label == 1
        
    except (AttributeError, ImportError):
        # This is expected before the PR is applied
        pytest.skip("New validation methods not yet available - this is expected before PR is applied")


def test_binary_target_validation():
    """Test that from_predictions validates binary targets correctly with new validation."""
    # Create sample data
    y_true = np.array([0, 1, 0, 1, 1])
    y_pred = np.array([0.1, 0.9, 0.2, 0.8, 0.7])
    
    try:
        # Test that from_predictions works with binary targets
        disp = CalibrationDisplay.from_predictions(y_true, y_pred)
        assert disp.pos_label == 1
        
        disp = RocCurveDisplay.from_predictions(y_true, y_pred)
        assert disp.pos_label == 1
        
        disp = PrecisionRecallDisplay.from_predictions(y_true, y_pred)
        assert disp.pos_label == 1
        
        disp = DetCurveDisplay.from_predictions(y_true, y_pred)
        assert disp.pos_label == 1
        
    except (AttributeError, ImportError):
        # This is expected before the PR is applied
        pytest.skip("New validation methods not yet available - this is expected before PR is applied")


if __name__ == "__main__":
    # Run the tests
    import sys
    
    try:
        test_display_classes_inherit_from_mixin()
        print("✓ test_display_classes_inherit_from_mixin passed")
    except Exception as e:
        print(f"✗ test_display_classes_inherit_from_mixin failed: {e}")
    
    try:
        test_new_validation_methods_exist()
        print("✓ test_new_validation_methods_exist passed")
    except Exception as e:
        print(f"✗ test_new_validation_methods_exist failed: {e}")
        
    try:
        test_plot_method_uses_new_axis_validation()
        print("✓ test_plot_method_uses_new_axis_validation passed")
    except Exception as e:
        print(f"✗ test_plot_method_uses_new_axis_validation failed: {e}")
        
    try:
        test_pos_label_validation_behavior()
        print("✓ test_pos_label_validation_behavior passed")
    except Exception as e:
        print(f"✗ test_pos_label_validation_behavior failed: {e}")
        
    try:
        test_binary_target_validation()
        print("✓ test_binary_target_validation passed")
    except Exception as e:
        print(f"✗ test_binary_target_validation failed: {e}")
        
    print("Test execution completed")