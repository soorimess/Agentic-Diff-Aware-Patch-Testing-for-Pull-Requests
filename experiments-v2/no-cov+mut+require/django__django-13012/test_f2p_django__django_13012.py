import unittest

from django.db.models import Value, ExpressionWrapper, IntegerField
from django.test import TestCase


class TestExpressionWrapperGroupBy(TestCase):
    def test_expression_wrapper_constant_should_not_be_in_group_by(self):
        """
        Test that ExpressionWrapper with constant expressions does not include
        the constant in GROUP BY clause.
        
        This is a regression test for the bug where ExpressionWrapper would
        incorrectly include constant expressions in GROUP BY clauses.
        """
        # Create a Value expression (constant) 
        value_expr = Value(3, output_field=IntegerField())
        
        # Create ExpressionWrapper around the Value expression
        wrapper_expr = ExpressionWrapper(value_expr, output_field=IntegerField())
        
        # Before the fix, wrapper_expr.get_group_by_cols() would return [wrapper_expr]
        # After the fix, it should return [] like the wrapped Value expression
        wrapper_group_by_cols = wrapper_expr.get_group_by_cols()
        
        # The fix ensures that constant expressions (Value) wrapped in ExpressionWrapper
        # don't appear in GROUP BY clauses, just like they don't when not wrapped
        self.assertEqual(wrapper_group_by_cols, [])