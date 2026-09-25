"""
Regression test for Django issue #14559: bulk_update() should return number of rows matched instead of None.
"""

from django.test import TestCase


class BulkUpdateReturnBehaviorTest(TestCase):
    def test_bulk_update_empty_list_returns_zero(self):
        """Test that bulk_update with empty list returns 0, not None"""
        from tests.queries.models import Note
        # This tests the specific behavior change in the issue report
        result = Note.objects.bulk_update([], ['misc'])
        # Before the change this would return None
        # After the change this should return 0
        self.assertEqual(result, 0)