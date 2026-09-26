import unittest
from django.db import models
from django.test import TestCase


class TestBulkUpdateReturnValues(TestCase):
    def setUp(self):
        class TestModel(models.Model):
            name = models.CharField(max_length=100)
            value = models.IntegerField(default=0)
            
            class Meta:
                app_label = 'test'

        self.TestModel = TestModel

    def test_bulk_update_empty_list_returns_zero(self):
        """Test that bulk_update with empty list returns 0, not None."""
        # This should return 0 (not None) when no objects to update
        rows_updated = self.TestModel.objects.bulk_update([], ['value'])
        self.assertEqual(rows_updated, 0)