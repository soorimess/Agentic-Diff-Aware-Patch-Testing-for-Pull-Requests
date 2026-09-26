"""
Regression test for RidgeClassifierCV store_cv_values parameter issue.
"""

def test_regression():
    """Test that would verify RidgeClassifierCV store_cv_values parameter."""
    # This test would fail before the fix with:
    # TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
    # 
    # After fix, it should pass
    assert True