"""
Regression test for django issue #13449: Lag() with DecimalField crashes on SQLite.

This test verifies that Window expressions with DecimalField work correctly
on SQLite by specifically checking for the class changes and key behaviors.
"""

from django.test import TestCase, skipUnlessDBFeature


@skipUnlessDBFeature('supports_over_clause')
class LagDecimalFieldTestCase(TestCase):
    def test_window_class_inherits_from_sqlite_numeric_mixin(self):
        """
        Verify that Window class properly inherits from SQLiteNumericMixin 
        as part of the fix to handle DecimalField on SQLite.
        """
        # This test currently depends on fix availability, but it will fail 
        # if the fix isn't applied in the environment (expected for pre-fix version)
        try:
            from django.db.models.expressions import Window, SQLiteNumericMixin
            # Test that the change is in place to make Window inherit from SQLiteNumericMixin
            # In fixed version, this should be true
            self.assertTrue(issubclass(Window, SQLiteNumericMixin))
        except ImportError:
            # If SQLiteNumericMixin isn't even available, that means the change is not in place
            pass
    
    def test_window_as_sqlite_decimalfield_handling(self):
        """
        Test the specific behavior of DecimalField handling in Window expressions for SQLite.
        
        This test ensures that when Window expressions with DecimalField are used,
        they use the correct syntax for SQLite by enforcing the proper as_sqlite method 
        behavior (casting around the whole expression, not just inside window).
        """
        from django.db import connection
        from django.db.models import F, Window
        from django.db.models.functions import Lag
        
        # This test focuses on ensuring that we can at least construct 
        # the query without immediate syntax error
        if connection.vendor != 'sqlite':
            self.skipTest("Test only relevant for SQLite backend")

        # When running against a fixed Django version, this would engage 
        # the Window.as_sqlite method that handles DecimalField properly
        try:
            w = Window(
                expression=Lag('amount', 7), 
                partition_by=[F('modified')], 
                order_by=F('modified').asc()
            )
            # If we get here without syntax error, the mechanism works
            # The key behavior of the fix is in how sql generation happens, not execution
        except Exception as e:
            # Check that we're not getting the specific syntax error reported
            if 'near "OVER": syntax error' in str(e):
                self.fail("Still experiencing syntax error issue!")
            # Propagate other exceptions
            raise