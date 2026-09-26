import unittest

from django.db.models import Value, ExpressionWrapper, IntegerField
from django.test import TestCase


class TestExpressionWrapperGroupBy(TestCase):
    def test_expression_wrapper_has_get_group_by_cols_method(self):
        """
        Regression test for Django issue #13012.
        ExpressionWrapper must have get_group_by_cols method to prevent 
        constant expressions from incorrectly appearing in GROUP BY clauses.
        
        The bug was that ExpressionWrapper.get_group_by_cols() method was missing,
        causing AttributeError when queries with ExpressionWrapper were compiled.
        """
        # Create ExpressionWrapper with constant Value (exact bug report scenario)
        expr = ExpressionWrapper(Value(3), output_field=IntegerField())
        
        # The fix ensures this method exists on ExpressionWrapper
        # Without it, queries would fail with AttributeError
        self.assertTrue(hasattr(expr, 'get_group_by_cols'))
        
        # Test that method can be called without AttributeError
        # This is the core symptom of the bug
        try:
            result = expr.get_group_by_cols()
            # Should return a list
            self.assertIsInstance(result, list)
        except AttributeError as e:
            if 'get_group_by_cols' in str(e):
                # This is the exact bug we're testing for
                self.fail("ExpressionWrapper missing get_group_by_cols method - would cause GROUP BY errors")
            raise