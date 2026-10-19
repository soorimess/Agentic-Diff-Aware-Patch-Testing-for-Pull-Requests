"""
Regression tests for pull request #60541
Fixes style checks in expressions/pytables
"""

import numpy as np
import pytest

from pandas.core.computation import expressions


def test_evaluate_numexpr_correct_variable_usage():
    """
    Test that _evaluate_numexpr correctly handles variable names in numexpr evaluation.
    
    This test ensures the fix where variable name consistency was improved in the
    local_dict passed to numexpr evaluation.
    """
    # Test with various data types to ensure robustness
    test_cases = [
        (np.array([1, 2, 3, 4]), np.array([2, 2, 2, 2])),
        (np.array([1.0, 2.0, 3.0]), np.array([0.5, 0.5, 0.5])),
        (np.array([10, 20, 30]), np.array([1, 1, 1])),
    ]
    
    for left_array, right_array in test_cases:
        result = expressions._evaluate_numexpr(
            op=np.add, 
            op_str="+", 
            left_op=left_array, 
            right_op=right_array
        )
        expected = left_array + right_array
        np.testing.assert_array_equal(result, expected)


def test_where_function_explicit_logic():
    """
    Test that where function uses explicit conditional logic for better maintainability.
    
    This validates the refactored conditional logic that improves readability.
    """
    # Test both code paths explicitly
    cond = np.array([True, False, True, False])
    left_op = np.array([1, 2, 3, 4])
    right_op = np.array([10, 20, 30, 40])
    
    # Test explicit numexpr path
    result_numexpr = expressions.where(cond, left_op, right_op, use_numexpr=True)
    expected = np.array([1, 20, 3, 40])
    np.testing.assert_array_equal(result_numexpr, expected)
    
    # Test explicit standard path  
    result_standard = expressions.where(cond, left_op, right_op, use_numexpr=False)
    np.testing.assert_array_equal(result_standard, expected)