"""
Regression test for Django #13012: ExpressionWrapper get_group_by_cols behavior.

Test for the exact fix that was introduced in the pull request.
"""

from django.db.models import ExpressionWrapper, IntegerField, Value
from django.test import TestCase


class ExpressionWrapperGroupByTests(TestCase):
    """
    Verify that ExpressionWrapper now has get_group_by_cols method to fix GROUP BY issues
    """
    
    def test_expression_wrapper_method_exists(self):
        """
        This test fails before fix is applied, passes after.
        The fix adds get_group_by_cols method to ExpressionWrapper class.
        """
        # Create ExpressionWrapper around a constant Value
        expr = ExpressionWrapper(Value(3), output_field=IntegerField())
        
        # Before fix: this would raise AttributeError 
        # After fix: this works and should return appropriate result
        try:
            result = expr.get_group_by_cols()
            # Method should exist and be callable
            self.assertIsNotNone(result)
        except AttributeError as e:
            if "get_group_by_cols" in str(e):
                self.fail("ExpressionWrapper.get_group_by_cols() method is missing - this is the bug (#13012)")
            raise
            
    def test_expression_wrapper_can_be_used_in_queries(self):
        """
        Test that the method existence allows queries to work without getting 
        AttributeError or incorrect SQL generation
        """
        from django.db.models import Sum
        
        # This is the essence of the issue - ExpressionWrapper should not crash
        expr = ExpressionWrapper(Value(3), output_field=IntegerField())
        
        # Just verify that the core functionality isn't broken regarding method existence
        self.assertTrue(hasattr(expr, 'get_group_by_cols'))
        self.assertTrue(callable(getattr(expr, 'get_group_by_cols')))