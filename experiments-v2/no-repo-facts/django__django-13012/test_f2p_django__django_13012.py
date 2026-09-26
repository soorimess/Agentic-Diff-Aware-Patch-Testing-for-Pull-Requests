"""
Regression test for Django ExpressionWrapper GROUP BY bug.

This test verifies that ExpressionWrapper properly delegates get_group_by_cols 
to its wrapped expression, preventing constants from appearing in GROUP BY clauses.

Before fix: ExpressionWrapper(Value(3)).get_group_by_cols() returns [ExpressionWrapper(Value(3))]
After fix: ExpressionWrapper(Value(3)).get_group_by_cols() returns []
"""
from django.test import TestCase
from django.db.models import Value, IntegerField
from django.db.models.expressions import ExpressionWrapper


class ExpressionWrapperGroupByTest(TestCase):
    def test_expression_wrapper_constant_group_by_regression(self):
        """
        Regression test for Django bug where ExpressionWrapper with constant expressions
        incorrectly places the constant in GROUP BY clause.
        
        This test ensures that when a constant expression is wrapped in ExpressionWrapper,
        the wrapper properly delegates group_by_cols handling to avoid including
        the constant in SQL GROUP BY clauses.
        """
        # Create constant expression that causes the bug
        constant_expr = Value(3, output_field=IntegerField())
        
        # Wrap it with ExpressionWrapper (as in the bug report)
        wrapped_expr = ExpressionWrapper(constant_expr, output_field=IntegerField())
        
        # Get group by columns for both
        unwrapped_group_by = constant_expr.get_group_by_cols()
        wrapped_group_by = wrapped_expr.get_group_by_cols()
        
        # The fix ensures these are equivalent
        # Before fix: unwrapped_group_by = [], wrapped_group_by = [ExpressionWrapper(Value(3))]
        # After fix: both should be []
        self.assertEqual(
            unwrapped_group_by, 
            wrapped_group_by,
            "ExpressionWrapper should delegate get_group_by_cols to wrapped expression"
        )
        
        # Additional verification: wrapped expression should not include itself
        self.assertNotIn(
            wrapped_expr,
            wrapped_group_by,
            "ExpressionWrapper should not include itself in group_by_cols"
        )