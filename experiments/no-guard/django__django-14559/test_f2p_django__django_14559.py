"""
Regression test for Django issue 14559.

bulk_update() should return the number of rows matched/updated,
not None like it did before.
"""
from django.test import TestCase


class TestBulkUpdateReturn(TestCase):
    def test_bulk_update_empty_list_returns_zero(self):
        """
        Test that bulk_update() returns 0 (not None) for empty object lists.
        
        The bug: bulk_update() returned None instead of row count
        The fix: bulk_update() returns 0 for empty lists, count for non-empty
        """
        from django.db import models
        
        class TestModel(models.Model):
            name = models.CharField(max_length=100)
            value = models.IntegerField(default=0)
            
            class Meta:
                app_label = 'test'
                db_table = 'test_bulk_update'

        # This verifies the fix - empty bulk_update should return 0, not None
        result = TestModel.objects.bulk_update([], ['name', 'value'])
        self.assertEqual(result, 0)