import unittest
from django.db.models import ExpressionWrapper, Value, IntegerField
from django.test import TestCase


class ExpressionWrapperGroupByTest(TestCase):
    def test_expression_wrapper_get_group_by_cols_delegation(self):
        """
        Test that ExpressionWrapper properly delegates get_group_by_cols to wrapped expressions.
        This test specifically checks that the delegation works correctly and that
        constant expressions don't appear in GROUP BY clauses.
        """
        # Create a constant expression
        constant_expr = Value(3, output_field=IntegerField())
        
        # Wrap it in ExpressionWrapper
        wrapped_expr = ExpressionWrapper(constant_expr, output_field=IntegerField())
        
        # Test that get_group_by_cols method exists and works correctly
        # In the fixed version, this should delegate properly to the wrapped expression
        group_by_cols = wrapped_expr.get_group_by_cols()
        
        # Value expressions should not contribute to GROUP BY clauses
        # So the result should be an empty list
        self.assertEqual(group_by_cols, [], 
                        "ExpressionWrapper with constant Value should not contribute to GROUP BY")
        
        # Also test with an alias parameter to make sure it's properly passed through
        group_by_cols_with_alias = wrapped_expr.get_group_by_cols(alias="test_alias")
        self.assertEqual(group_by_cols_with_alias, [], 
                        "ExpressionWrapper with constant Value should not contribute to GROUP BY even with alias")
    
    def test_expression_wrapper_method_exists(self):
        """
        Test that ExpressionWrapper has the get_group_by_cols method.
        """
        # Create a constant expression
        constant_expr = Value(3, output_field=IntegerField())
        
        # Wrap it in ExpressionWrapper
        wrapped_expr = ExpressionWrapper(constant_expr, output_field=IntegerField())
        
        # The method should exist and be callable
        self.assertTrue(hasattr(wrapped_expr, 'get_group_by_cols'))
        
        # Test that calling it doesn't raise AttributeError
        try:
            wrapped_expr.get_group_by_cols()
            # If we get here without exception, the method exists and works
        except AttributeError:
            self.fail("ExpressionWrapper.get_group_by_cols() method is missing - this is the bug!")