import unittest
from django.db import models
from django.db.models import F
from django.db.models.functions import Lag
from django.db.models import Window
from django.test import TestCase


class LagDecimalFieldTest(TestCase):
    def test_window_inherits_from_sqlite_numeric_mixin(self):
        """Test that Window class inherits from SQLiteNumericMixin (the fix)."""
        # This test specifically checks the inheritance change that was made in the fix
        # Before the fix: Window class did not inherit from SQLiteNumericMixin  
        # After the fix: Window class inherits from SQLiteNumericMixin
        
        from django.db.models.expressions import Window, SQLiteNumericMixin
        
        # Check if Window inherits from SQLiteNumericMixin
        window_class = Window
        inherits_from_sqlite_numeric = any(cls is SQLiteNumericMixin or SQLiteNumericMixin in cls.__mro__ 
                                          for cls in window_class.__mro__)
        
        # This assertion will fail before the fix and pass after the fix
        # This is the core behavior change that fixes the bug
        self.assertTrue(inherits_from_sqlite_numeric, 
                       "Window class should inherit from SQLiteNumericMixin to fix Lag with DecimalField on SQLite")
        
    def test_window_has_as_sqlite_method(self):
        """Test that Window class has the as_sqlite method that was added in the fix."""
        # The fix adds an as_sqlite method to Window class
        from django.db.models.expressions import Window
        
        # Check if Window has as_sqlite method
        window_class = Window
        has_as_sqlite = hasattr(window_class, 'as_sqlite')
        
        # This should be True after the fix is applied
        # The method is what handles the specific case of DecimalField in window expressions
        self.assertTrue(has_as_sqlite, "Window class should have as_sqlite method for SQLite handling")
        
    def test_window_with_lag_decimalfield_structure(self):
        """Test that Window with Lag on DecimalField has correct structure."""
        # Create a model with DecimalField
        class LagTest(models.Model):
            modified = models.DateField()
            amount = models.DecimalField(decimal_places=4, max_digits=7)
            
            class Meta:
                app_label = 'test'
        
        # Create a window expression with Lag on DecimalField
        # This is the exact case that was failing in the bug report
        w = Window(
            expression=Lag('amount', 7), 
            partition_by=[F('modified')], 
            order_by=F('modified').asc()
        )
        
        # Verify the window expression components
        self.assertIsNotNone(w)
        self.assertIsNotNone(w.source_expression)
        self.assertEqual(w.source_expression.function, 'LAG')
        
    def test_lag_function_window_compatibility(self):
        """Test that Lag function is properly window compatible."""
        # Test that Lag is window compatible
        lag_func = Lag('amount', 7)
        self.assertTrue(hasattr(lag_func, 'window_compatible'))
        self.assertTrue(lag_func.window_compatible)
        
        # Test that it has the right function name
        self.assertEqual(lag_func.function, 'LAG')