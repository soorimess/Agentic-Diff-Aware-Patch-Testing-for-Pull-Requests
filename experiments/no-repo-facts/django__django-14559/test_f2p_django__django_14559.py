"""
Regression test for Django bulk_update() return value behavior.

This tests that bulk_update() returns the number of rows matched (like update())
rather than None.
"""

from django.test import TestCase
from .models import Note


class BulkUpdateReturnValueTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.notes = [Note.objects.create(note=str(i), misc=str(i)) for i in range(5)]

    def test_bulk_update_returns_number_of_rows(self):
        """Test that bulk_update returns the number of rows updated."""
        # Test with existing objects
        for note in self.notes:
            note.note = 'updated-' + note.note
            
        # This should return the number of rows updated (5)
        result = Note.objects.bulk_update(self.notes, ['note'])
        self.assertEqual(result, 5)
        
    def test_bulk_update_empty_queryset_returns_zero(self):
        """Test that bulk_update with empty queryset returns 0."""
        # This should return 0 for empty objects list
        result = Note.objects.bulk_update([], ['note'])
        self.assertEqual(result, 0)