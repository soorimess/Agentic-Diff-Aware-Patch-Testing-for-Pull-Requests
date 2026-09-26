import unittest

from django.db.models import ExpressionWrapper, Value
from django.test import TestCase


class TestExpressionWrapperGroupBy(TestCase):
    """Test that ExpressionWrapper properly handles GROUP BY clauses."""

    def test_expression_wrapper_get_group_by_cols_method_exists(self):
        """
        Test that ExpressionWrapper has get_group_by_cols method that delegates properly.
        
        Before the fix, ExpressionWrapper would not have a get_group_by_cols method,
        causing it to fall back to the base Expression class behavior which would
        incorrectly include the ExpressionWrapper in GROUP BY clauses.
        
        This is a regression test for Django ticket #13012.
        """
        # Create a Value expression (constant) 
        value_expr = Value(3)
        
        # Create an ExpressionWrapper around it
        wrapper_expr = ExpressionWrapper(value_expr, output_field=None)
        
        # Test that the wrapper has get_group_by_cols method
        # This should not raise AttributeError
        self.assertTrue(hasattr(wrapper_expr, 'get_group_by_cols'))
        
        # Test the behavior - before the fix, this would return [wrapper_expr]
        # after the fix, this should return [] (delegating to the wrapped Value)
        wrapper_group_by = wrapper_expr.get_group_by_cols()
        
        # The fix should make ExpressionWrapper delegate to its wrapped expression
        # Value expressions should return empty list from get_group_by_cols (constants don't go in GROUP BY)
        # So wrapper should also return empty list
        self.assertEqual(wrapper_group_by, [])