"""
Tests for the edit_only feature in model formsets.
When edit_only=True is specified, formsets should not create new objects.
"""

from django.test import TestCase
from django.forms.models import modelformset_factory
from tests.model_formsets.models import Author


class ModelFormsetEditOnlyTests(TestCase):
    def test_edit_only_prevents_new_objects(self):
        # Create existing author to edit
        existing_author = Author.objects.create(name="Original Name")
        
        # Create formset with edit_only=True - should only edit existing objects
        AuthorFormSet = modelformset_factory(Author, fields=['name'], edit_only=True)
        
        # Submit data that includes both existing and a new object to create
        data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '1',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': str(existing_author.id),
            'form-0-name': 'Updated Name',
            'form-1-name': 'New Author Name',  # Should not be created when edit_only=True
        }
        
        formset = AuthorFormSet(data)
        
        # Validate formset 
        self.assertTrue(formset.is_valid())
        
        # Save the formset
        saved_objects = formset.save()
        
        # With edit_only=True, should only return existing object
        self.assertEqual(len(saved_objects), 1)
        self.assertEqual(saved_objects[0].id, existing_author.id)
        self.assertEqual(saved_objects[0].name, "Updated Name")
        
        # New author should NOT be created in database
        new_authors = Author.objects.filter(name="New Author Name")
        self.assertEqual(new_authors.count(), 0)
        
        # Existing author should be updated
        updated_author = Author.objects.get(id=existing_author.id)
        self.assertEqual(updated_author.name, "Updated Name")