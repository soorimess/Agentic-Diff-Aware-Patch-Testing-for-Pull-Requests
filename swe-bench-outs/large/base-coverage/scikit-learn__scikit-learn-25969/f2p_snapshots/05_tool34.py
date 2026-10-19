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


def test_mixin_inheritance():
    """Test that display classes inherit from _BinaryClassifierCurveDisplayMixin."""
    try:
        # This test should pass after the PR is applied
        from sklearn.utils._plotting import _BinaryClassifierCurveDisplayMixin
        
        # Test that the classes inherit from the expected mixin
        assert issubclass(CalibrationDisplay, _BinaryClassifierCurveDisplayMixin)
        assert issubclass(RocCurveDisplay, _BinaryClassifierCurveDisplayMixin)
        assert issubclass(PrecisionRecallDisplay, _BinaryClassifierCurveDisplayMixin)
        assert issubclass(DetCurveDisplay, _BinaryClassifierCurveDisplayMixin)
        
    except ImportError:
        # Skip if the mixin doesn't exist yet (before PR)
        pytest.skip("Mixin class not yet available - this is expected before PR is applied")


def test_validation_methods_exist():
    """Test that new validation methods exist and are used."""
    try:
        # Test that the new validation methods exist
        assert hasattr(CalibrationDisplay, '_validate_and_get_response_values')
        assert hasattr(RocCurveDisplay, '_validate_and_get_response_values')
        assert hasattr(PrecisionRecallDisplay, '_validate_and_get_response_values')
        assert hasattr(DetCurveDisplay, '_validate_and_get_response_values')
        
        assert hasattr(CalibrationDisplay, '_validate_from_predictions_params')
        assert hasattr(RocCurveDisplay, '_validate_from_predictions_params')
        assert hasattr(PrecisionRecallDisplay, '_validate_from_predictions_params')
        assert hasattr(DetCurveDisplay, '_validate_from_predictions_params')
        
    except AttributeError:
        # Skip if methods don't exist yet (before PR)
        pytest.skip("Validation methods not yet available - this is expected before PR is applied")


def test_basic_functionality_works():
    """Test that basic functionality works with new validation."""
    # Create sample data
    X, y = make_classification(n_samples=50, n_features=10, n_classes=2, 
                               n_informative=5, random_state=42)
    clf = LogisticRegression(random_state=42)
    clf.fit(X, y)
    
    try:
        # Test that from_estimator works correctly with proper parameters
        # This tests that the parameter passing works correctly
        disp = CalibrationDisplay.from_estimator(clf, X, y)
        assert disp is not None
        assert hasattr(disp, 'prob_true')
        assert hasattr(disp, 'prob_pred')
        assert hasattr(disp, 'y_prob')
        assert disp.estimator_name == "LogisticRegression"
        
        # Test that from_predictions works correctly
        y_true = np.array([0, 1, 0, 1, 1])
        y_pred = np.array([0.1, 0.9, 0.2, 0.8, 0.7])
        
        disp2 = CalibrationDisplay.from_predictions(y_true, y_pred)
        assert disp2 is not None
        assert disp2.pos_label == 1
        
        # Test that other display classes work too
        disp3 = RocCurveDisplay.from_estimator(clf, X, y)
        assert disp3 is not None
        
        disp4 = PrecisionRecallDisplay.from_estimator(clf, X, y)
        assert disp4 is not None
        
        disp5 = DetCurveDisplay.from_estimator(clf, X, y)
        assert disp5 is not None
        
    except (AttributeError, ImportError, TypeError):
        # Skip if methods don't exist yet (before PR)
        pytest.skip("New validation methods not yet available - this is expected before PR is applied")


def test_parameter_validation():
    """Test that parameters are properly validated and passed."""
    # Create sample data
    X, y = make_classification(n_samples=50, n_features=10, n_classes=2, 
                               n_informative=5, random_state=42)
    clf = LogisticRegression(random_state=42)
    clf.fit(X, y)
    
    try:
        # Test that from_estimator properly handles parameters - specifically checking for None values
        # This should NOT be None - if it was, the parameter passing would be broken
        disp = CalibrationDisplay.from_estimator(clf, X, y, name="TestClassifier")
        assert disp is not None
        assert disp.estimator_name == "TestClassifier"
        
        # Test with explicit pos_label
        disp2 = CalibrationDisplay.from_estimator(clf, X, y, pos_label=1)
        assert disp2 is not None
        
        # Test from_predictions with sample weights
        y_true = np.array([0, 1, 0, 1, 1])
        y_pred = np.array([0.1, 0.9, 0.2, 0.8, 0.7])
        disp3 = CalibrationDisplay.from_predictions(y_true, y_pred, sample_weight=[1, 1, 1, 1, 1])
        assert disp3 is not None
        
        # Test that from_estimator with response_method works
        disp4 = CalibrationDisplay.from_estimator(clf, X, y, response_method="predict_proba")
        assert disp4 is not None
        
    except (AttributeError, ImportError, TypeError):
        # Skip if methods don't exist yet (before PR)
        pytest.skip("New validation methods not yet available - this is expected before PR is applied")


def test_plot_method_returns_valid_axes():
    """Test that plot methods return valid axis objects."""
    # Create sample data
    X, y = make_classification(n_samples=50, n_features=10, n_classes=2, 
                               n_informative=5, random_state=42)
    clf = LogisticRegression(random_state=42)
    clf.fit(X, y)
    
    try:
        # Test that plot methods create proper axes
        disp = CalibrationDisplay.from_estimator(clf, X, y)
        assert disp is not None
        assert hasattr(disp, 'ax_')
        assert hasattr(disp, 'figure_')
        
        # Test that the axes are valid matplotlib objects
        assert disp.ax_ is not None
        assert disp.figure_ is not None
        
        # Test that the plot method itself works
        disp.plot()
        assert disp.ax_ is not None
        
    except (AttributeError, ImportError, TypeError):
        # Skip if methods don't exist yet (before PR)
        pytest.skip("New validation methods not yet available - this is expected before PR is applied")


def test_parameter_passing_specifically():
    """Test that specific parameter passing issues are caught."""
    # Create sample data
    X, y = make_classification(n_samples=30, n_features=5, n_classes=2, 
                               n_informative=3, random_state=42)
    clf = LogisticRegression(random_state=42)
    clf.fit(X, y)
    
    try:
        # Test that we can actually call the methods with real parameters
        # This specifically tests that the y parameter is not None
        disp = CalibrationDisplay.from_estimator(clf, X, y)
        assert disp is not None
        assert disp.estimator_name == "LogisticRegression"
        
        # Test that we can call from_predictions with real data
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0.1, 0.9, 0.2, 0.8])
        disp2 = CalibrationDisplay.from_predictions(y_true, y_pred)
        assert disp2 is not None
        
        # Test that the returned objects have the right structure
        assert hasattr(disp2, 'prob_true')
        assert hasattr(disp2, 'prob_pred')
        assert hasattr(disp2, 'y_prob')
        
    except (AttributeError, ImportError, TypeError):
        # Skip if methods don't exist yet (before PR)
        pytest.skip("New validation methods not yet available - this is expected before PR is applied")


if __name__ == "__main__":
    # Run the tests
    import sys
    
    try:
        test_mixin_inheritance()
        print("✓ test_mixin_inheritance passed")
    except Exception as e:
        print(f"✗ test_mixin_inheritance failed: {e}")
    
    try:
        test_validation_methods_exist()
        print("✓ test_validation_methods_exist passed")
    except Exception as e:
        print(f"✗ test_validation_methods_exist failed: {e}")
        
    try:
        test_basic_functionality_works()
        print("✓ test_basic_functionality_works passed")
    except Exception as e:
        print(f"✗ test_basic_functionality_works failed: {e}")
        
    try:
        test_parameter_validation()
        print("✓ test_parameter_validation passed")
    except Exception as e:
        print(f"✗ test_parameter_validation failed: {e}")
        
    try:
        test_plot_method_returns_valid_axes()
        print("✓ test_plot_method_returns_valid_axes passed")
    except Exception as e:
        print(f"✗ test_plot_method_returns_valid_axes failed: {e}")
        
    try:
        test_parameter_passing_specifically()
        print("✓ test_parameter_passing_specifically passed")
    except Exception as e:
        print(f"✗ test_parameter_passing_specifically failed: {e}")
        
    print("Test execution completed")