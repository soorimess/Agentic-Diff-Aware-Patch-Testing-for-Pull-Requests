"""
Regression test for Django Window + Lag + DecimalField SQLite issue.

This tests the specific bug where Window expressions containing Lag with
DecimalField would generate invalid SQL on SQLite, causing an OperationalError.
"""
import datetime
from django.db import models
from django.db.models import F, Window
from django.db.models.functions import Lag
from django.test import TestCase, skipUnlessDBFeature


class LagTestModel(models.Model):
    modified = models.DateField()
    data = models.FloatField()
    amount = models.DecimalField(decimal_places=4, max_digits=7)

    class Meta:
        app_label = 'test'


@skipUnlessDBFeature('supports_over_clause')
class WindowDecimalFieldRegressionTest(TestCase):
    """
    Test to ensure Window with Lag and DecimalField works correctly on SQLite.
    This is a regression test for the bug that caused OperationalError.
    """
    
    @classmethod
    def setUpTestData(cls):
        # Create test data matching bug report scenario
        LagTestModel.objects.create(
            modified=datetime.date(2020, 1, 1),
            data=10.5,
            amount=123.4567
        )
        LagTestModel.objects.create(
            modified=datetime.date(2020, 1, 1),
            data=20.3,
            amount=234.5678
        )
        LagTestModel.objects.create(
            modified=datetime.date(2020, 1, 2),
            data=30.1,
            amount=345.6789
        )

    def test_lag_with_decimalfield_no_crash(self):
        """
        Test that Window expression with Lag on DecimalField doesn't crash on SQLite.
        
        This tests the specific scenario from the bug report that would cause:
        OperationalError: near "OVER": syntax error
        """
        # Exact scenario from bug report
        w = Window(
            expression=Lag('amount', 7),
            partition_by=[F('modified')], 
            order_by=F('modified').asc()
        )
        
        # This query previously crashed with OperationalError
        queryset = LagTestModel.objects.all().annotate(w=w)
        
        # Should execute successfully (this is the behavior change being tested)
        results = list(queryset)
        
        # Verify it returns the expected number of records
        self.assertEqual(len(results), 3)