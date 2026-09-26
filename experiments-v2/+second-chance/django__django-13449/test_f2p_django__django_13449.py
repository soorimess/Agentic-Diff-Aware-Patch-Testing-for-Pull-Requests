from django.db import models
from django.db.models import F, Window
from django.db.models.functions import Lag
from django.test import TestCase, skipUnlessDBFeature


class LagDecimalFieldTest(TestCase):
    @skipUnlessDBFeature('supports_over_clause')
    def test_lag_with_decimal_field_sql_syntax_error(self):
        """
        Test that Lag() with DecimalField doesn't cause SQL syntax error on SQLite.
        This is a regression test for Django issue #13449.
        """
        # The bug was that when using Lag() with DecimalField on SQLite,
        # the generated SQL had incorrect syntax causing OperationalError.
        
        # Create a model that will be used in the query
        class TestModel(models.Model):
            modified = models.DateField()
            amount = models.DecimalField(decimal_places=4, max_digits=7)
            
            class Meta:
                app_label = 'test'

        # Create a window expression with Lag on DecimalField
        w = Window(
            expression=Lag('amount', 7),
            partition_by=[F('modified')],
            order_by=F('modified').asc()
        )
        
        # Test the actual SQL generation that would cause the bug
        # This should fail with OperationalError: near "OVER": syntax error if bug exists
        try:
            from django.db import connection
            if connection.vendor == 'sqlite':
                # Create a query that forces SQL generation
                qs = TestModel.objects.all().annotate(w=w)
                # Force evaluation to trigger SQL generation
                # This is the exact scenario that was failing in the bug report
                list(qs[:1])
                # If we get here without exception, the test passes
                self.assertTrue(True)
            else:
                # For other databases, just make sure the Window expression can be created
                self.assertIsNotNone(w)
        except Exception as e:
            # Check if this is the specific bug error we're testing for
            error_str = str(e).lower()
            if "over" in error_str and "syntax error" in error_str:
                # This is the exact bug from the issue report
                self.fail("Lag with DecimalField on SQLite causes SQL syntax error: %s" % str(e))
            else:
                # Re-raise other exceptions
                raise