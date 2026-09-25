"""
Regression test for Django issue #14559:
bulk_update() should return number of rows matched, not None.
"""
from django.db import transaction
from django.test import TestCase

from .queries.models import Note


class BulkUpdateReturnTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.notes = [Note.objects.create(note=str(i), misc=str(i)) for i in range(5)]

    def test_bulk_update_empty_list_returns_zero(self):
        """Test that bulk_update() returns 0 when given an empty list."""
        result = Note.objects.bulk_update([], ['note'])
        self.assertEqual(result, 0)

    def test_bulk_update_returns_row_count(self):
        """Test that bulk_update() returns the number of rows updated."""
        # Update all notes - should return 5
        for note in self.notes:
            note.note = 'test-%s' % note.id
        result = Note.objects.bulk_update(self.notes, ['note'])
        self.assertEqual(result, 5)

    def test_bulk_update_partial_update_returns_correct_count(self):
        """Test that bulk_update() returns correct count when updating partial set."""
        # Update only first 3 notes - should return 3
        subset = self.notes[:3]
        for note in subset:
            note.note = 'partial-%s' % note.id
        result = Note.objects.bulk_update(subset, ['note'])
        self.assertEqual(result, 3)