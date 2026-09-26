"""
Regression test for Django ticket #13012:
ExpressionWrapper with constant expressions incorrectly placed in GROUP BY clause.
"""
import unittest

from django.db.models import ExpressionWrapper, IntegerField, Sum, Value
from django.test import TestCase


class ExpressionWrapperGroupByTest(TestCase):
    def test_expression_wrapper_group_by_behavior(self):
        """
        Test that ExpressionWrapper properly handles group by columns for constant expressions.
        
        Before the fix, ExpressionWrapper(Value(3)) would incorrectly return 
        [ExpressionWrapper(Value(3))] from get_group_by_cols(), causing constants 
        to be included in GROUP BY clauses.
        
        After the fix, ExpressionWrapper(Value(3)) correctly returns [] from 
        get_group_by_cols(), because the wrapped Value(3) returns [].
        """
        # Create a Value expression (constant)
        value_expr = Value(3)
        
        # Create ExpressionWrapper around the constant Value
        wrapper_expr = ExpressionWrapper(value_expr, output_field=IntegerField())
        
        # Test the get_group_by_cols behavior
        value_group_by = value_expr.get_group_by_cols()
        wrapper_group_by = wrapper_expr.get_group_by_cols()
        
        # The Value expression should return an empty list (constants don't go in GROUP BY)
        self.assertEqual(value_group_by, [])
        
        # The ExpressionWrapper should also return an empty list after the fix
        # This is the key behavior that the fix enables
        # Before the fix, this would fail because it would return [wrapper_expr]
        self.assertEqual(wrapper_group_by, [])