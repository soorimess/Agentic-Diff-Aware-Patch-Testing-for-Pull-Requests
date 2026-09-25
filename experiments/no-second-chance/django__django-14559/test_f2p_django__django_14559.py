"""
Regression test for Django issue #14559.

Tests that bulk_update() now returns the number of rows affected,
consistent with update(), rather than returning None.
"""

from django.test import TestCase


class TestBulkUpdateReturnValues(TestCase):
    def test_bulk_update_empty_list_returns_zero_instead_of_none(self):
        """
        Test that bulk_update() with empty list returns 0 instead of None.
        
        This addresses the core bug reported: bulk_update() returns None,
        unlike update() which returns the number of rows matched.
        The fix ensures consistency by returning 0 for empty lists.
        """
        from django.db import models
        
        class TestModel(models.Model):
            name = models.CharField(max_length=100)
            
            class Meta:
                app_label = 'test'
                db_table = 'bulk_update_test'

        # Before the fix: bulk_update([]) returned None
        # After the fix: bulk_update([]) returns 0
        result = TestModel.objects.bulk_update([], ['name'])
        self.assertEqual(result, 0)