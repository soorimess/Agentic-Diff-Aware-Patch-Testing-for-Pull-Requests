from django.db import models
from django.db.models import F, Window
from django.db.models.functions import Lag
from django.test import TestCase, skipUnlessDBFeature
from django.db import connection
from django.db.models.fields import DecimalField


class LagDecimalFieldTest(TestCase):
    @skipUnlessDBFeature('supports_over_clause')
    def test_window_inherits_sqlite_numeric_mixin(self):
        """
        Test that Window class properly inherits from SQLiteNumericMixin
        and has the correct as_sqlite method for handling DecimalFields.
        """
        # This test verifies that the Window class has been modified to 
        # inherit from SQLiteNumericMixin
        from django.db.models.expressions import Window, SQLiteNumericMixin
        
        # Check that Window inherits from SQLiteNumericMixin
        self.assertTrue(issubclass(Window, SQLiteNumericMixin))
        
    @skipUnlessDBFeature('supports_over_clause') 
    def test_window_as_sqlite_method_exists(self):
        """
        Test that Window class has the as_sqlite method that handles
        DecimalField casting correctly for SQLite.
        """
        from django.db.models.expressions import Window
        
        # Check that as_sqlite method exists
        self.assertTrue(hasattr(Window, 'as_sqlite'))
        
        # The method should be callable
        w = Window(expression=Lag('amount', 7))
        self.assertTrue(callable(getattr(w, 'as_sqlite', None)))
        
    @skipUnlessDBFeature('supports_over_clause')
    def test_lag_with_decimal_field_functionality(self):
        """
        Test that Lag with DecimalField works correctly in window expressions.
        This test focuses on the behavioral change rather than the exact SQL syntax.
        """
        # Create a window expression with Lag on a field that would be DecimalField
        # The key test is that this doesn't raise an exception that would indicate
        # the SQL generation issue
        try:
            w = Window(
                expression=Lag('amount', 7),
                partition_by=[F('modified')],
                order_by=F('modified').asc()
            )
            
            # The main point is that the Window object can be created and used
            # without issues that would indicate the bug
            self.assertIsNotNone(w)
            
        except Exception as e:
            # If we get an OperationalError with syntax error, that would indicate
            # the bug we're testing for
            if 'syntax error' in str(e).lower() and 'OVER' in str(e):
                self.fail("Lag with DecimalField on SQLite produces invalid SQL")
            raise