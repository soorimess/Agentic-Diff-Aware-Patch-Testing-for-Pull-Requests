"""
Regression test for Django issue where ExpressionWrapper with constant expressions
incorrectly include the constant in GROUP BY clause.
"""
from django.db.models import Value, ExpressionWrapper, IntegerField
from django.test import TestCase


class TestExpressionWrapperGroupBy(TestCase):
    def test_expression_wrapper_group_by_cols(self):
        """
        Test that ExpressionWrapper properly delegates group_by_cols to inner expression.
        """
        # Value should not be included in GROUP BY
        value_expr = Value(3, output_field=IntegerField())
        expected_group_by_cols = value_expr.get_group_by_cols()
        self.assertEqual(expected_group_by_cols, [])
        
        # ExpressionWrapper should delegate to the inner expression
        wrapper_expr = ExpressionWrapper(value_expr, output_field=IntegerField())
        actual_group_by_cols = wrapper_expr.get_group_by_cols()
        
        # They should behave the same way
        self.assertEqual(actual_group_by_cols, expected_group_by_cols)