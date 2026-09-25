import unittest

from django.db.models import (
    ExpressionWrapper, IntegerField, Value
)
from django.test import SimpleTestCase


class TestExpressionWrapperGroupByBehavior(SimpleTestCase):
    def test_expression_wrapper_group_by_cols(self):
        """
        Test that ExpressionWrapper properly delegates get_group_by_cols to its expression.
        
        Before the fix, ExpressionWrapper didn't override get_group_by_cols, so it
        would return self instead of delegating to the wrapped expression.
        
        A Value expression should return an empty list from get_group_by_cols,
        meaning it should not be included in GROUP BY clauses.
        """
        # Create a Value expression (constant) - should return empty list
        const_expr = Value(3)
        const_group_by_cols = const_expr.get_group_by_cols()
        
        # Create an ExpressionWrapper around the constant
        wrapped_expr = ExpressionWrapper(const_expr, output_field=IntegerField())
        wrapped_group_by_cols = wrapped_expr.get_group_by_cols()
        
        # A Value expression should return empty list
        self.assertEqual(const_group_by_cols, [])
        
        # After the fix, ExpressionWrapper should delegate properly
        # Before the fix, wrapped_group_by_cols would be [wrapped_expr] 
        # After the fix, wrapped_group_by_cols should be [] (same as const_group_by_cols)
        self.assertEqual(wrapped_group_by_cols, [])