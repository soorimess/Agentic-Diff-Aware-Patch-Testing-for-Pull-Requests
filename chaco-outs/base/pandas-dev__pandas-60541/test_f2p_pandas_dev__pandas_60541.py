"""
Regression test for PR #60541: FIX: ruff checks in expressions/pytables

This test specifically validates the fix for the numexpr local_dict parameter 
where right_op was incorrectly used instead of right_value in expressions.py.

The fix ensures that when numexpr evaluates expressions like "left_value + right_value",
the local_dict correctly maps "right_value" to the variable named "right_value" 
rather than to the parameter named "right_op".
"""

import numpy as np
import operator

from pandas.core.computation import expressions


def test_evaluate_with_numexpr_local_dict_correctness():
    """
    Test that numexpr evaluation uses correct variable mapping in local_dict.
    
    This validates the specific fix where right_op was incorrectly used instead 
    of right_value in the local_dict parameter.
    """
    # Test with various operations to ensure correct variable mapping
    left_array = np.array([1, 2, 3])
    right_array = np.array([4, 5, 6])
    
    # Test addition
    result = expressions.evaluate(
        operator.add, left_array, right_array, use_numexpr=True
    )
    expected = np.array([5, 7, 9])
    np.testing.assert_array_equal(result, expected)
    
    # Test multiplication
    result = expressions.evaluate(
        operator.mul, left_array, right_array, use_numexpr=True
    )
    expected = np.array([4, 10, 18])
    np.testing.assert_array_equal(result, expected)
    
    # Test subtraction
    result = expressions.evaluate(
        operator.sub, left_array, right_array, use_numexpr=True
    )
    expected = np.array([-3, -3, -3])
    np.testing.assert_array_equal(result, expected)


def test_where_function_with_both_modes():
    """
    Test where function with both numexpr enabled and disabled modes.
    
    This validates the if-else structure change in the where function.
    """
    cond = np.array([True, False, True])
    left_array = np.array([1, 2, 3])
    right_array = np.array([4, 5, 6])
    
    # Test with numexpr enabled
    result_enabled = expressions.where(
        cond, left_array, right_array, use_numexpr=True
    )
    expected = np.array([1, 5, 3])
    np.testing.assert_array_equal(result_enabled, expected)
    
    # Test with numexpr disabled
    result_disabled = expressions.where(
        cond, left_array, right_array, use_numexpr=False
    )
    np.testing.assert_array_equal(result_disabled, expected)


def test_evaluate_with_different_data_types():
    """
    Test evaluate with different data types to ensure robustness.
    """
    # Test with float arrays
    left_float = np.array([1.5, 2.5, 3.5])
    right_float = np.array([4.5, 5.5, 6.5])
    
    result = expressions.evaluate(
        operator.add, left_float, right_float, use_numexpr=True
    )
    expected = np.array([6.0, 8.0, 10.0])
    np.testing.assert_array_equal(result, expected)
    
    # Test with integer arrays
    left_int = np.array([10, 20, 30])
    right_int = np.array([2, 4, 5])
    
    result = expressions.evaluate(
        operator.mul, left_int, right_int, use_numexpr=True
    )
    expected = np.array([20, 80, 150])
    np.testing.assert_array_equal(result, expected)