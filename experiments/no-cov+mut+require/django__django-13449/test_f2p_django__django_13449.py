"""
Regression test for Django ticket #13449: Lag() with DecimalField crashes on SQLite.

Tests that the specific structural fix was applied to correctly handle 
DecimalField in Window expressions on SQLite.
"""
from django.test import TestCase


class LagDecimalFieldRegressionTest(TestCase):
    """
    Test that verifies the Window class fix for DecimalField on SQLite.
    """
    
    def test_window_class_inheritance_from_sqlite_numeric_mixin(self):
        """
        Verify that Window class inherits from SQLiteNumericMixin.
        This validates the core structural change that fixes the bug.
        """
        from django.db.models.expressions import Window, SQLiteNumericMixin
        
        # Check if Window directly inherits from SQLiteNumericMixin
        # This is the key change from the bug fix: Window(SQLiteNumericMixin, Expression)
        # instead of just Window(Expression)
        
        window_bases = Window.__mro__
        has_sqlite_mixin = any(issubclass(cls, SQLiteNumericMixin) for cls in window_bases)
        
        # Before fix: Window only inherits from Expression
        # After fix: Window inherits from SQLiteNumericMixin, Expression
        self.assertTrue(has_sqlite_mixin, 
                       "Window class should inherit from SQLiteNumericMixin after fix")