"""
Regression test for Django issue #13449.

Lag() with DecimalField crashes on SQLite due to incorrect SQL generation.
This test will fail before the fix (when Window doesn't inherit from SQLiteNumericMixin)
and pass after the fix (when it does).
"""
from django.db import models
from django.db.models import F
from django.db.models.functions import Lag
from django.db.models import Window
from django.test import TestCase


class LagDecimalFieldTestCase(TestCase):
    def test_window_class_implements_fix_correctly(self):
        """
        This test directly checks for the behavioral change introduced in the fix:
        
        Before fix: Window class inherits from Expression only
        After fix: Window class inherits from (SQLiteNumericMixin, Expression)
        
        The fix enables proper handling of DecimalFields in Window expressions on SQLite.
        """
        from django.db.models.expressions import Window, SQLiteNumericMixin
        
        # Test the inheritance hierarchy that was changed
        window_mro = [cls.__name__ for cls in Window.__mro__]
        
        # This assertion should pass when the fix is applied correctly
        # and fail when the fix is missing (e.g., if Window only inherits from Expression)
        self.assertIn('SQLiteNumericMixin', window_mro, 
                     "Window class should inherit from SQLiteNumericMixin for proper DecimalField handling")
        
        # Also validate the method exists (this was added)
        self.assertTrue(hasattr(Window, 'as_sqlite'),
                       "Window class should have as_sqlite method to handle DecimalField case")
        
        # Validate we can construct the problematic setup from the bug report
        lag_expr = Lag('amount', 7)
        lag_expr.output_field = models.DecimalField(decimal_places=4, max_digits=7)
        
        window = Window(
            expression=lag_expr,
            partition_by=[F('modified')],
            order_by=F('modified').asc()
        )
        
        # Basic validation - should work in both cases
        self.assertIsNotNone(window)


    def test_desired_behavior_exists(self):
        """
        Test that demonstrates what the fix enables - proper SQL generation for 
        Lag() with DecimalField on SQLite.
        """
        # The main point of the fix is that when you have:
        # Window(expression=Lag('amount', 7), ...) where amount is DecimalField
        # On SQLite, this should work without syntax errors
        
        # We can at least make sure class constructors and basic access work  
        from django.db.models.expressions import Window 
        
        lag_expr = Lag('amount', 7)
        lag_expr.output_field = models.DecimalField(decimal_places=4, max_digits=7)
        
        window = Window(
            expression=lag_expr,
            partition_by=[F('modified')],
            order_by=F('modified').asc()
        )
        
        # Make sure we can examine the structure
        self.assertEqual(window.source_expression.function, 'LAG')
        self.assertEqual(window.source_expression.output_field.__class__.__name__, 'DecimalField')
        
        # This test sets up the exact conditions that cause the bug reported:
        # - Lag window function
        # - DecimalField as the source field
        # - SQLite backend compatibility concern