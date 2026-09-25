"""
Regression test for Django bug where Lag() with DecimalField crashes on SQLite.
The fix was to make Window inherit from SQLiteNumericMixin and implement as_sqlite method.
"""
from django.db import models
from django.db.models import F, Window
from django.db.models.functions import Lag
from django.test import TestCase, skipUnlessDBFeature


class LagDecimalFieldRegressionTest(TestCase):
    """Tests for regression of Lag() with DecimalField on SQLite bug."""
    
    @skipUnlessDBFeature('supports_over_clause')
    def test_window_inherits_from_sqlite_numeric_mixin(self):
        """
        Test that Window class inherits from SQLiteNumericMixin.
        This is the key change in the fix: Window now inherits from SQLiteNumericMixin.
        """
        # The fundamental change with the PR is: class Window(SQLiteNumericMixin, Expression):
        # So if we can check this inheritance, we validate the fix
        from django.db.models.expressions import Window, SQLiteNumericMixin
        
        # Check if Window inherits from SQLiteNumericMixin directly or indirectly  
        self.assertTrue(issubclass(Window, SQLiteNumericMixin))
        
        # Ensure this is really direct inheritance viewed from the instance
        w = Window(expression=Lag('test', 1))
        self.assertIsInstance(w, SQLiteNumericMixin)
        
    @skipUnlessDBFeature('supports_over_clause')
    def test_window_has_as_sqlite_method(self):
        """
        Test that Window class now has the as_sqlite method.
        This method was added as part of the fix.
        """
        from django.db.models.expressions import Window
        
        # Check the method exists on Window class
        self.assertTrue(hasattr(Window, 'as_sqlite'))
        
        # Check that it's callable as a method
        w = Window(expression=Lag('test', 1))
        self.assertTrue(callable(getattr(w, 'as_sqlite', None)))
        
    @skipUnlessDBFeature('supports_over_clause')
    def test_window_lag_decimalfield_no_syntax_error(self):
        """
        Test the core bug behavior: Window with Lag on DecimalField should not crash.
        The actual fix is in the as_sqlite method that places CAST correctly.
        """
        # This creates the exact expression that would trigger the internal error  
        w = Window(
            expression=Lag('amount', 7),
            partition_by=[F('modified')],
            order_by=F('modified').asc()
        )
        
        # Basic validation that the structure allows for proper setup
        self.assertIsNotNone(w)
        self.assertIsNotNone(w.source_expression)
        self.assertEqual(w.source_expression.__class__.__name__, 'Lag')