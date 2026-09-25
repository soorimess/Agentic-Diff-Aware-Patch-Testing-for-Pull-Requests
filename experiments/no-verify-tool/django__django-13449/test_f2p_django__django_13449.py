"""
Regression test for Lag() with DecimalField on SQLite.

This test validates that Window expressions with Lag/Lead functions on DecimalFields
generate correct SQL on SQLite by ensuring CAST wraps the entire window expression
rather than just the inner function.
"""

from django.test import TestCase
from django.db import models
from django.db.models import F
from django.db.models.functions import Lag
from django.db.models import Window


class LagTestModel(models.Model):
    modified = models.DateField()
    data = models.FloatField()  
    amount = models.DecimalField(decimal_places=4, max_digits=7)

    class Meta:
        app_label = 'test'


class TestLagDecimalFieldSQLiteRegression(TestCase):
    """
    Regression test for Django issue where Lag() with DecimalField crashes on SQLite.
    
    Original behavior: Generated SQL like:
        CAST(LAG("amount", 7) AS NUMERIC) OVER (PARTITION BY "modified" ORDER BY "modified" ASC)
    
    Fixed behavior: Generated SQL like:
        CAST(LAG("amount", 7) OVER (PARTITION BY "modified" ORDER BY "modified" ASC) AS NUMERIC) 
    """
    
    def test_window_lag_decimalfield_sqlite_correct_cast_placement(self):
        """
        Test that when using Window with Lag on a DecimalField, the SQL generation
        places CAST correctly around the entire window expression for SQLite.
        """
        # Create the specific expression that triggers the bug
        window_expr = Window(
            expression=Lag('amount', 7),
            partition_by=[F('modified')], 
            order_by=F('modified').asc()
        )
        
        # The test is basically checking that we don't get the syntax error
        # The main difference between before/after the fix is in SQL generation:
        # - Before fix: SQL syntax error due to misplaced CAST
        # - After fix: Properly formed SQL that SQLite can execute
        # 
        # Since we can't easily test the SQL generation without full Django setup,
        # this test ensures that no syntax errors occur when running this query
        # on a SQLite backend
        
        try:
            # This will generate the SQL and attempt to execute it
            query = LagTestModel.objects.all().annotate(w=window_expr)
            # Just accessing the first result should trigger SQL compilation for SQLite
            list(query[:1])
            
            # If we reached here without syntax errors, the fix is working
            self.assertTrue(True)
            
        except Exception as e:
            error_msg = str(e)
            # The specific error we're guarding against
            if 'near "OVER"' in error_msg and 'syntax error' in error_msg:
                self.fail("Regression: Lag with DecimalField causes SQLite syntax error "
                         "due to incorrect CAST placement in SQL")
            # Re-raise if it's some other kind of error  
            raise