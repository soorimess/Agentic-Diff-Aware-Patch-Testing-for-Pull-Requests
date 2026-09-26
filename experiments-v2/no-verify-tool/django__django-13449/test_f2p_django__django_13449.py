import unittest
from django.db import models
from django.db.models import F, Window
from django.db.models.functions import Lag
from django.test import TestCase, skipUnlessDBFeature


class LagDecimalFieldTest(TestCase):
    @skipUnlessDBFeature('supports_over_clause')
    def test_lag_with_decimal_field_on_sqlite(self):
        """Test that Lag() with DecimalField works correctly on SQLite."""
        # Create a model with DecimalField as described in the bug report
        class LagTest(models.Model):
            modified = models.DateField()
            data = models.FloatField()
            amount = models.DecimalField(decimal_places=4, max_digits=7)
            
            class Meta:
                app_label = 'test_f2p_django__django_13449'
        
        # Create the window expression as described in the bug report
        w = Window(
            expression=Lag('amount', 7), 
            partition_by=[F('modified')], 
            order_by=F('modified').asc()
        )
        
        # This should not raise an OperationalError on SQLite
        # The bug was that it would generate invalid SQL with CAST applied incorrectly
        # The fix ensures that DecimalField casting happens properly outside the window clause
        try:
            # This query should work without OperationalError
            qs = LagTest.objects.all().annotate(w=w)
            # Force evaluation to trigger SQL execution
            list(qs)
            # If we get here without exception, the test passes
        except Exception as e:
            # If we get an OperationalError with "near OVER: syntax error", 
            # that's the bug we're testing for
            if 'OVER' in str(e) and 'syntax error' in str(e).lower():
                self.fail("Lag with DecimalField on SQLite raises syntax error: %s" % e)
            raise


if __name__ == '__main__':
    unittest.main()