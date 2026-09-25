"""
Regression test for ExpressionWrapper GROUP BY issue.
Tests that constant expressions within ExpressionWrapper are not included in GROUP BY clause.
"""
from django.db.models import ExpressionWrapper, IntegerField, Value
from django.test import TestCase


class ExpressionWrapperGroupByTestCase(TestCase):
    def test_expression_wrapper_constant_value_not_in_group_by(self):
        """
        Test that ExpressionWrapper with a constant Value expression does not 
        include the constant in the GROUP BY clause.
        
        This is a regression test for a bug where ExpressionWrapper would incorrectly
        include constant expressions in GROUP BY clauses, causing PostgreSQL errors
        like "aggregate functions are not allowed in GROUP BY".
        """
        # Create a Value expression (constant)  
        value_expr = Value(3, output_field=IntegerField())
        
        # Create an ExpressionWrapper around it 
        wrapped_expr = ExpressionWrapper(value_expr, output_field=IntegerField())
        
        # Value expressions should return empty list for group_by_cols (constants don't go in GROUP BY)
        self.assertEqual(value_expr.get_group_by_cols(), [])
        
        # ExpressionWrapper's get_group_by_cols method should delegate to the inner expression
        # so that constant expressions are properly excluded from GROUP BY
        self.assertEqual(wrapped_expr.get_group_by_cols(), [])
        
        # Verify the behavior that would have caused the original bug:
        # Before fix, this would return [ExpressionWrapper(Value(3))] 
        # After fix, this correctly returns [] 
        # This is what we're asserting to prevent regression