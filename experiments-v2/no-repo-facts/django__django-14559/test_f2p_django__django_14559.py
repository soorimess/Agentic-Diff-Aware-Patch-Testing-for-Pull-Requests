import unittest

from django.test import TestCase

from .models import Note


class BulkUpdateReturnValuesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.notes = [
            Note.objects.create(note=str(i), misc=str(i))
            for i in range(5)
        ]

    def test_bulk_update_empty_list_returns_zero(self):
        """
        bulk_update() should return 0 when called with an empty list,
        matching the behavior of update().
        """
        # Test with empty list - should return 0, not None
        result = Note.objects.bulk_update([], ['note'])
        self.assertEqual(result, 0)

    def test_bulk_update_returns_number_of_rows_updated(self):
        """
        bulk_update() should return the number of rows updated,
        matching the behavior of update().
        """
        # Modify some notes
        for note in self.notes:
            note.note = 'updated-%s' % note.id
            
        # Should return the number of rows updated (5)
        result = Note.objects.bulk_update(self.notes, ['note'])
        self.assertEqual(result, 5)