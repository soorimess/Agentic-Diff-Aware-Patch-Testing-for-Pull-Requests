import unittest

from django.db.models import ExpressionWrapper, Value, IntegerField
from django.test import TestCase


class Django13012Test(TestCase):
    def test_expression_wrapper_constant_in_group_by(self):
        """
        Test that ExpressionWrapper with constant expressions does not include
        the constant in GROUP BY clause.
        This test verifies the fix for the bug where constant expressions in 
        ExpressionWrapper were incorrectly included in GROUP BY clauses.
        """
        # Create a Value expression (constant) 
        value_expr = Value(3, output_field=IntegerField())
        
        # Wrap it in ExpressionWrapper
        wrapped_expr = ExpressionWrapper(value_expr, output_field=IntegerField())
        
        # Before the fix, the get_group_by_cols method would return the ExpressionWrapper itself
        # After the fix, it should delegate to the wrapped expression
        # A Value expression should not contribute to GROUP BY (it's a constant)
        group_by_cols = wrapped_expr.get_group_by_cols()
        
        # This assertion will fail before the fix and pass after the fix
        # The bug was that group_by_cols would contain 1 item (the ExpressionWrapper itself)
        # instead of 0 items (empty list)
        self.assertEqual(len(group_by_cols), 0, 
                         "ExpressionWrapper with constant Value should not contribute to GROUP BY")