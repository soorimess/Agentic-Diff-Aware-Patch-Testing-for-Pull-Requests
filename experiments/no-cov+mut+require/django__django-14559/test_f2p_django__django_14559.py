"""
Regression test for Django issue #14559:
bulk_update() should return number of rows matched/updated like update() does.

The fix makes bulk_update() return 0 when given empty list, and integer count
when given objects instead of returning None.
"""

from django.test import TestCase

# Import from the same location as the other tests
from .queries.models import Note


class BulkUpdateReturnTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.notes = [Note.objects.create(note=str(i), misc=str(i)) for i in range(5)]

    def test_bulk_update_returns_count_not_none(self):
        """
        bulk_update() should return count of rows updated, not None.
        
        Before fix: bulk_update() returned None
        After fix: bulk_update() returns integer count of rows updated
        """
        # Test with actual data - should return count instead of None
        for note in self.notes:
            note.note = 'updated-%s' % note.id
            
        result = Note.objects.bulk_update(self.notes, ['note'])
        
        # This assertion should be true after fix, false before fix
        self.assertIsNotNone(result)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 5)

    def test_bulk_update_empty_list_returns_zero(self):
        """
        bulk_update([]) should return 0, not None.
        """
        result = Note.objects.bulk_update([], ['note'])
        
        # This assertion should be true after fix, false before fix  
        self.assertEqual(result, 0)