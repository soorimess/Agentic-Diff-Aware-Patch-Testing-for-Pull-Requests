from django.test import TestCase

from .models import Note


class BulkUpdateReturnValuesTest(TestCase):
    def test_bulk_update_empty_list_returns_zero(self):
        """Test that bulk_update returns 0 when passed an empty list."""
        # Test with empty list - should return 0, not None
        result = Note.objects.bulk_update([], ['note'])
        self.assertEqual(result, 0)

    def test_bulk_update_returns_number_of_rows_updated(self):
        """Test that bulk_update returns the number of rows updated."""
        # Create some test objects
        notes = [
            Note.objects.create(note=str(i), misc=str(i))
            for i in range(3)
        ]
        
        # Update them
        for note in notes:
            note.note = note.note + '_updated'
            note.misc = note.misc + '_updated'

        # Test that bulk_update returns the correct count
        result = Note.objects.bulk_update(notes, ['note', 'misc'])
        
        # Should return the number of objects updated (3)
        self.assertEqual(result, 3)