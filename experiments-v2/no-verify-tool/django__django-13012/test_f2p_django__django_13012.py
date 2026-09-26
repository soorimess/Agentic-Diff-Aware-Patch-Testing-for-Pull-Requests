import unittest

from django.db.models import ExpressionWrapper, IntegerField, Value


class Django13012Test(unittest.TestCase):
    def test_expression_wrapper_get_group_by_cols_delegates_to_wrapped_expression(self):
        """
        Regression test for Django #13012.
        
        ExpressionWrapper.get_group_by_cols() should delegate to the wrapped expression's
        get_group_by_cols() method, not return itself.
        
        Before the fix, ExpressionWrapper would return [self] instead of delegating,
        causing constant expressions to incorrectly appear in GROUP BY clauses.
        """
        # Create a Value expression (constant)
        value_expr = Value(3, output_field=IntegerField())
        
        # Create ExpressionWrapper around the Value expression
        wrapper_expr = ExpressionWrapper(value_expr, output_field=IntegerField())
        
        # The Value expression should not be included in GROUP BY columns
        # because it's a constant that doesn't depend on grouping
        expected_group_by_cols = []  # Value expressions should return empty list
        
        # This is what the buggy behavior would return (incorrect)
        buggy_result = [wrapper_expr]  # This is what was happening before the fix
        
        # This is what the correct behavior should return (after the fix)
        correct_result = expected_group_by_cols
        
        # Test the actual behavior
        actual_group_by_cols = wrapper_expr.get_group_by_cols()
        
        # The bug is that it returns [wrapper_expr] instead of []
        self.assertEqual(
            actual_group_by_cols, 
            correct_result,
            f"ExpressionWrapper.get_group_by_cols() should delegate to wrapped expression. "
            f"Expected {correct_result}, but got {actual_group_by_cols}"
        )
        
        # Verify that the buggy behavior would have been wrong
        self.assertNotEqual(
            actual_group_by_cols,
            buggy_result,
            "This would be the buggy behavior - ExpressionWrapper returning itself"
        )