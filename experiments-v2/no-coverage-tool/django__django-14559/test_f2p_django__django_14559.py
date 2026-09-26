"""
Regression test for Django issue #14559:
bulk_update() should return the number of rows matched, not None.
"""
from django.test import TestCase


class BulkUpdateReturnTest(TestCase):
    def test_bulk_update_behavior_change(self):
        """
        Test that bulk_update() returns integer count instead of None.
        This verifies the fix for Django issue #14559.
        """
        # Import model
        from queries.models import Note
        
        # Test with data
        note1 = Note.objects.create(note="test", misc="misc")
        note1.note = "updated"
        
        # This should return integer count, not None
        result = Note.objects.bulk_update([note1], ['note'])
        
        # These assertions verify the behavior change:
        # Before fix: result would be None (causing assertion failures)
        # After fix: result would be integer (passing assertions)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1)