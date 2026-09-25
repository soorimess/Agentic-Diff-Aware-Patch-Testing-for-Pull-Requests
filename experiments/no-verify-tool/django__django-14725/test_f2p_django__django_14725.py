"""
Regression tests for Django ticket #14725:
Provide a way for model formsets to disallow new object creation.
"""
from django.test import TestCase
from django.db import models
from django.forms.models import modelformset_factory


class TestModel(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(default=0)


class EditOnlyFormSetTests(TestCase):
    def test_edit_only_formset_ignores_new_objects(self):
        """
        Verify that edit_only=True prevents creation of new objects even when data is submitted.
        Regression test for Django #14725.
        """
        # Create a formset with edit_only=True
        FormSet = modelformset_factory(
            TestModel,
            fields=['name', 'value'],
            edit_only=True
        )
        
        # Create an existing object
        existing_obj = TestModel.objects.create(name="Existing", value=10)
        
        # Create formset data with both existing and new object data
        data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '1',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': str(existing_obj.id),
            'form-0-name': 'Updated',
            'form-0-value': '20',
            'form-1-name': 'New Object',
            'form-1-value': '30',
        }
        
        # The edit_only formset should only process existing object, disregard new one
        formset = FormSet(data=data)
        self.assertTrue(formset.is_valid())
        
        # Save the formset 
        saved_objects = formset.save(commit=True)
        
        # Only the existing object should be returned (updated)
        self.assertEqual(len(saved_objects), 1)
        self.assertEqual(saved_objects[0].id, existing_obj.id)
        self.assertEqual(saved_objects[0].name, "Updated") 
        self.assertEqual(saved_objects[0].value, 20)
        
        # New object should not have been created
        self.assertEqual(TestModel.objects.count(), 1)
        
    def test_normal_formset_creates_new_objects(self):
        """
        Verify that normal formsets (edit_only=False) still create new objects.
        This ensures we're not breaking existing behavior.
        """
        # Create a formset with default edit_only=False (should be same as explicit False)
        FormSet = modelformset_factory(
            TestModel,
            fields=['name', 'value'],
            edit_only=False  # Explicitly show default
        )
        
        # Create an existing object
        existing_obj = TestModel.objects.create(name="Existing", value=10)
        
        # Create formset data with both existing and new object data
        data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '1',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': str(existing_obj.id),
            'form-0-name': 'Updated',
            'form-0-value': '20',
            'form-1-name': 'New Object',
            'form-1-value': '30',
        }

        # The normal formset should create new objects
        formset = FormSet(data=data)
        self.assertTrue(formset.is_valid())
        
        # Save the formset
        saved_objects = formset.save(commit=True)
        
        # Both objects should be returned (updated existing + created new)
        self.assertEqual(len(saved_objects), 2)
        
        # Verify one is the updated existing object
        updated_obj = None
        new_obj = None
        for obj in saved_objects:
            if obj.id == existing_obj.id:
                updated_obj = obj
            else:
                new_obj = obj
                
        self.assertIsNotNone(updated_obj)
        self.assertIsNotNone(new_obj)
        self.assertEqual(updated_obj.name, "Updated")
        self.assertEqual(updated_obj.value, 20)
        self.assertEqual(new_obj.name, "New Object")
        self.assertEqual(new_obj.value, 30)
        
        # Both objects should exist
        self.assertEqual(TestModel.objects.count(), 2)