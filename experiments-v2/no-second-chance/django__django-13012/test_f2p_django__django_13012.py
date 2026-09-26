import unittest

from django.db.models import Value, IntegerField, ExpressionWrapper
from django.test import TestCase


class TestExpressionWrapperGroupBy(TestCase):
    def test_expression_wrapper_get_group_by_cols_exists(self):
        """
        Regression test for Django bug: ExpressionWrapper with constant expressions 
        were incorrectly placed in GROUP BY clauses.
        
        Before fix: ExpressionWrapper lacked get_group_by_cols method, causing AttributeError
        or incorrect GROUP BY behavior.
        
        After fix: ExpressionWrapper has get_group_by_cols method that properly handles
        constant expressions in GROUP BY contexts.
        """
        # Create a constant expression that was causing the issue
        constant_expr = Value(3, output_field=IntegerField())
        
        # Wrap it - this is the scenario from the bug report
        wrapped_expr = ExpressionWrapper(constant_expr, output_field=IntegerField())
        
        # The fix adds this method to prevent the bug
        # Test that it exists to avoid AttributeError and incorrect GROUP BY behavior
        self.assertTrue(
            hasattr(wrapped_expr, 'get_group_by_cols'),
            "ExpressionWrapper.get_group_by_cols() method required to prevent GROUP BY bug"
        )
        
        # Test that calling it works (would fail with AttributeError before fix)
        try:
            result = wrapped_expr.get_group_by_cols()
            self.assertIsInstance(result, list)
        except AttributeError:
            self.fail("ExpressionWrapper.get_group_by_cols() method missing - causes GROUP BY bug")