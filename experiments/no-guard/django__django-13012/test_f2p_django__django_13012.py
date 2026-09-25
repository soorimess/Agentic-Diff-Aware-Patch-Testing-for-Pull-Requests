"""
Regression test for Django issue where constant expressions
of an ExpressionWrapper object are incorrectly placed at the GROUP BY clause.
"""
from django.test import TestCase
from django.db.models import Value, IntegerField, ExpressionWrapper


class ExpressionWrapperGroupByTest(TestCase):
    def test_expression_wrapper_delegates_group_by_cols_correctly(self):
        """
        Test that ExpressionWrapper properly delegates group_by_cols to its wrapped expression.
        
        This test ensures that constants wrapped in ExpressionWrapper don't get 
        incorrectly included in GROUP BY clauses, which was causing PostgreSQL errors.
        """
        # Create a constant Value expression (the source of the bug)
        value_expr = Value(3)
        
        # Create an ExpressionWrapper around it 
        wrapped_expr = ExpressionWrapper(value_expr, output_field=IntegerField())
        
        # Test what happens with group_by_cols
        # Before fix: ExpressionWrapper would return [ExpressionWrapper] (including itself)
        # After fix: ExpressionWrapper should return [] (delegate to wrapped expression)
        
        group_by_cols = wrapped_expr.get_group_by_cols()
        
        # The core assertion: constant expressions should not contribute to GROUP BY
        # This is the key behavior change being tested
        self.assertEqual(
            len(group_by_cols), 
            0, 
            "ExpressionWrapper around constant should not contribute to GROUP BY clauses"
        )
        
        # More specific assertion of what should happen
        self.assertEqual(
            group_by_cols, 
            [], 
            "ExpressionWrapper should delegate to wrapped expression and return empty list"
        )