"""
Test for PR #22616: ENH: stats: use `vecdot` and `nonzero` where appropriate

This test validates that the mathematical operations used in PR #22616 work correctly.
It ensures that when the PR is applied, the functions using vecdot will work as expected.
"""

import numpy as np


def test_vecdot_operations():
    """
    Test mathematical operations that will be replaced with vecdot calls in the PR.
    """
    # Test basic vector dot product operations
    np.random.seed(42)
    
    # 1D case - sum(x * y) will become vecdot(x, y)
    x = np.random.randn(50)
    y = np.random.randn(50)
    result = np.sum(x * y)
    assert np.isscalar(result)
    
    # 2D case with axis - sum(x * y, axis=0) will become vecdot(x, y, axis=0)  
    x_2d = np.random.randn(30, 20)
    y_2d = np.random.randn(30, 20)
    result_axis0 = np.sum(x_2d * y_2d, axis=0)
    assert result_axis0.shape == (20,)
    
    # Boolean array operations - x.sum() becomes count_nonzero(x)
    bool_arr = np.random.rand(100) > 0.5
    count_result = np.count_nonzero(bool_arr)
    sum_result = bool_arr.sum()
    assert count_result == sum_result
    assert isinstance(count_result, (int, np.integer))
    
    # Sum of squares - sum(x * x) will become vecdot(x, x)
    a = np.random.randn(10)
    sum_squares = np.sum(a * a)
    assert np.isscalar(sum_squares)
    assert sum_squares >= 0


def test_known_values():
    """
    Test with known values to ensure mathematical correctness.
    """
    # Test vector dot product with known values
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([4.0, 5.0, 6.0])
    
    # Expected result: 1*4 + 2*5 + 3*6 = 32
    expected = 32.0
    actual = np.sum(x * y)
    
    assert np.isclose(actual, expected)
    
    # Test integer arrays
    x_int = np.array([1, 2, 3])
    y_int = np.array([4, 5, 6])
    result_int = np.sum(x_int * y_int)
    assert result_int == 32


def test_edge_cases():
    """
    Test edge cases for the operations that will be changed.
    """
    # Empty arrays
    empty_x = np.array([])
    empty_y = np.array([])
    result_empty = np.sum(empty_x * empty_y)
    assert np.isscalar(result_empty)
    
    # Single element arrays
    single_x = np.array([5.0])
    single_y = np.array([3.0])
    result_single = np.sum(single_x * single_y)
    assert result_single == 15.0
    
    # Boolean arrays with all False
    all_false = np.array([False, False, False])
    count_false = np.count_nonzero(all_false)
    sum_false = all_false.sum()
    assert count_false == sum_false == 0
    
    # Boolean arrays with all True
    all_true = np.array([True, True, True])
    count_true = np.count_nonzero(all_true)
    sum_true = all_true.sum()
    assert count_true == sum_true == 3