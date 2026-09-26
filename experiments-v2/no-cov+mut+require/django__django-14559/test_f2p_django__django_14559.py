"""
Regression test for Django issue #14559:
Include number of rows matched in bulk_update() return value
"""
from django.test import TestCase


class BulkUpdateReturnTest(TestCase):
    def test_bulk_update_returns_number_of_rows_updated(self):
        """
        Test that bulk_update() returns the number of rows updated, 
        matching the behavior of update().
        """
        # This test will be run by Django's test runner which will handle imports
        
        # Create test data - we'll test the return value behavior
        from tests.queries.models import Note
        
        # Create some test data
        notes = [Note.objects.create(note=str(i), misc=str(i)) for i in range(5)]
        
        # Modify the notes
        for note in notes:
            note.note = 'updated-%s' % note.id
            
        # Test that bulk_update returns the number of rows updated (should be 5)
        # Before fix: would return None
        # After fix: should return 5
        updated_count = Note.objects.bulk_update(notes, ['note'])
        
        # The key assertion - the return value should be the count of updated rows
        self.assertEqual(updated_count, 5)
        
    def test_bulk_update_returns_zero_when_no_objects(self):
        """
        Test that bulk_update() returns 0 when no objects are provided.
        """
        from tests.queries.models import Note
        
        # Test with empty list - should return 0 (not None)
        updated_count = Note.objects.bulk_update([], ['note'])
        self.assertEqual(updated_count, 0)