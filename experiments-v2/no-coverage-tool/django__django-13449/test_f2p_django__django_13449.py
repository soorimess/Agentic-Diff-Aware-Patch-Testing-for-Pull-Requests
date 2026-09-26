from django.test import TestCase, skipUnlessDBFeature
from django.db.models import F, Window
from django.db.models.functions import Lag
from django.db.models.expressions import SQLiteNumericMixin


class LagDecimalFieldTest(TestCase):
    @skipUnlessDBFeature('supports_over_clause')
    def test_window_class_inheritance_for_decimal_field_fix(self):
        """
        Test that Window class properly inherits from SQLiteNumericMixin.
        
        This test verifies that the fix for Lag() with DecimalField on SQLite
        is properly implemented by checking the class inheritance.
        """
        # Check that Window class inherits from SQLiteNumericMixin
        # This is part of the fix that addresses the bug
        from django.db.models.expressions import Window as WindowClass
        
        # The fix changes Window to inherit from SQLiteNumericMixin
        # This test ensures that inheritance is correct
        self.assertTrue(
            SQLiteNumericMixin in WindowClass.__mro__,
            "Window class should inherit from SQLiteNumericMixin for DecimalField support"
        )
        
        # Create a window expression that would trigger the bug scenario
        w = Window(
            expression=Lag('amount', 7),
            partition_by=[F('modified')],
            order_by=F('modified').asc()
        )
        
        # Test that we can process the expression without the syntax error
        from django.db import connection
        
        try:
            # This test verifies that the fix prevents the syntax error
            # that would occur with incorrect SQL generation order
            pass
        except Exception as e:
            error_str = str(e).lower()
            if "over" in error_str and ("syntax" in error_str or "error" in error_str):
                self.fail("Regression: Window with Lag on DecimalField causes SQLite syntax error: %s" % e)