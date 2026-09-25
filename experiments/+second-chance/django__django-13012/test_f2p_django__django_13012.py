"""
Regression test for ExpressionWrapper get_group_by_cols bug.

This test verifies that ExpressionWrapper instances properly delegate 
get_group_by_cols() to their wrapped expressions, preventing constants
from being incorrectly included in GROUP BY clauses.
"""
from django.db.models import Value, ExpressionWrapper, IntegerField
from django.test import SimpleTestCase


class TestExpressionWrapperGroupBy(SimpleTestCase):
    def test_constant_expression_wrapper_not_in_group_by(self):
        """
        Test that constant expressions wrapped in ExpressionWrapper 
        do not appear in GROUP BY clauses.
        
        Before fix: ExpressionWrapper.get_group_by_cols() would return the 
        ExpressionWrapper itself, causing constants to be incorrectly included
        in GROUP BY clauses in PostgreSQL and other databases.
        
        After fix: ExpressionWrapper.get_group_by_cols() correctly delegates
        to the wrapped expression's get_group_by_cols() method.
        """
        # Create a constant value expression
        value_expr = Value(3, output_field=IntegerField())
        
        # Wrap it in ExpressionWrapper
        wrapped_expr = ExpressionWrapper(value_expr, output_field=IntegerField())
        
        # The fix ensures this returns [] (empty) - constants should not be in GROUP BY
        # Before the fix, this would incorrectly return [wrapped_expr]
        group_by_cols = wrapped_expr.get_group_by_cols()
        
        # If this assertion passes, the fix works correctly 
        self.assertEqual(
            group_by_cols,
            [],
            "Constant expressions in ExpressionWrapper should not be in GROUP BY clause"
        )