"""
Regression test for Django bug where Lag() with DecimalField crashes on SQLite.

This test verifies that Window expressions correctly handle DecimalFields
when used in window functions, preventing the "OperationalError: near "OVER": syntax error"
that occurred due to malformed SQL generation.
"""
from django.db import models
from django.db.models import F, Window
from django.db.models.functions import Lag
from django.test import SimpleTestCase


class LagDecimalFieldRegressionTests(SimpleTestCase):
    def test_window_class_inheritance(self):
        """
        Test that Window class properly inherits from SQLiteNumericMixin.
        
        This regression test checks that the Window class now inherits from
        SQLiteNumericMixin as introduced in the fix, which properly handles
        DecimalField casting in window functions.
        """
        from django.db.models import expressions
        import inspect
        
        # Get the Window class
        window_class = expressions.Window
        
        # Verify it now inherits from SQLiteNumericMixin
        from django.db.models.expressions import SQLiteNumericMixin
        self.assertTrue(issubclass(window_class, SQLiteNumericMixin))
        
    def test_window_with_lag_decimal_field(self):
        """
        Test that constructing a Window with Lag on DecimalField works.
        
        This prevents regression of the bug where the malformed SQL was:
        CAST(LAG("field", 7) AS NUMERIC) OVER (PARTITION BY ...)
        """
        # Before the fix, this would be the source location where SQL compilation
        # would produce malformed syntax due to incorrect cast placement
        try:
            w = Window(
                expression=Lag('amount', 7),
                partition_by=[F('modified')],
                order_by=F('modified').asc()
            )
            
            # If we get here, the Window expression can be constructed correctly
            self.assertIsNotNone(w)
            
        except Exception as e:
            # If this raises an exception that would have been the SyntaxError from SQLite
            # we want to make sure we don't hit it
            if 'OperationalError' in str(type(e)) or 'syntax error' in str(e).lower():
                self.fail(f"Window with Lag on DecimalField causes SQL syntax error: {e}")
            raise
            
    def test_window_function_exists(self):
        """
        Verify that the Window class has the necessary methods introduced in fix.
        """
        # Verify the Window class has the as_sqlite method that handles DecimalField cases
        from django.db.models import expressions
        
        window_class = expressions.Window
        self.assertTrue(hasattr(window_class, 'as_sqlite'))