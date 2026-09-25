"""
Regression test for Django issue #14559: bulk_update() should return the number of
rows matched, like update() does.
"""
from django.test import TestCase
from django.db import models


class TestNote(models.Model):
    note = models.CharField(max_length=100)
    misc = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'test'


class BulkUpdateReturnValuesTest(TestCase):
    def test_bulk_update_returns_zero_for_empty_list(self):
        """
        bulk_update() should return 0 when given an empty list of objects,
        not None.
        """
        # This should return 0, but currently returns None
        result = TestNote.objects.bulk_update([], ['note'])
        self.assertEqual(result, 0)

    def test_bulk_update_returns_number_of_updated_rows(self):
        """
        bulk_update() should return the number of rows updated, not None.
        """
        # Create some test objects
        notes = [TestNote.objects.create(note=str(i), misc=str(i)) for i in range(5)]
        
        # Modify the objects
        for note in notes:
            note.note = 'updated-%s' % note.id
        
        # bulk_update should return the number of rows updated (5 in this case)
        # Currently it returns None, so this would fail anyway 
        result = TestNote.objects.bulk_update(notes, ['note'])
        self.assertEqual(result, 5)