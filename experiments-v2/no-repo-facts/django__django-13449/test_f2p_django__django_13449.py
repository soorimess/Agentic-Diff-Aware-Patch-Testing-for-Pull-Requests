"""
Test for Django issue #13449: Lag() with DecimalField crashes on SQLite.

This test reproduces the bug where using Lag() with a DecimalField in a Window
expression causes an OperationalError on SQLite due to incorrect SQL generation.
"""
from django.db import models
from django.db.models import F, Window
from django.db.models.functions import Lag
from django.test import TestCase, skipUnlessDBFeature


class LagTestModel(models.Model):
    modified = models.DateField()
    data = models.FloatField()
    amount = models.DecimalField(decimal_places=4, max_digits=7)

    class Meta:
        app_label = 'expressions_window'


@skipUnlessDBFeature('supports_over_clause')
class LagDecimalFieldTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.test_instance = LagTestModel.objects.create(
            modified='2023-01-01',
            data=10.5,
            amount=123.4567
        )

    def test_lag_with_decimal_field_on_sqlite(self):
        """
        Test that Lag() with DecimalField works correctly on SQLite.
        
        This should not raise an OperationalError about syntax error near "OVER".
        """
        # This is the exact query from the bug report that was failing
        w = Window(
            expression=Lag('amount', 7), 
            partition_by=[F('modified')], 
            order_by=F('modified').asc()
        )
        
        # This should not raise an OperationalError
        queryset = LagTestModel.objects.all().annotate(w=w)
        
        # Try to evaluate the query to trigger the SQL generation
        list(queryset)
        
        # If we get here without exception, the test passes
        self.assertTrue(True)