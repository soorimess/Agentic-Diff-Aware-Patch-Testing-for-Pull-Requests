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
        """bulk_update() should return 0 when given an empty list."""
        # Before fix: returned None
        # After fix: should return 0
        result = self.TestModel.objects.bulk_update([], ['name'])
        self.assertEqual(result, 0)