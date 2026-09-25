"""
Regression test for Django issue #14725: Provide a way for model formsets to disallow new object creation.
"""
from django.test import TestCase
from django.forms.models import modelformset_factory
from tests.model_formsets.models import Author


class EditOnlyFormsetTests(TestCase):
    def test_edit_only_formset_has_edit_only_attribute(self):
        """Test that formset has edit_only attribute when edit_only=True is specified."""
        # This should work after the fix is applied - checking edit_only parameter
        FormSet = modelformset_factory(
            Author, 
            fields=['name'], 
            edit_only=True
        )
        
        # Create an instance and check the edit_only attribute
        formset = FormSet()
        self.assertTrue(hasattr(formset, 'edit_only'))
        self.assertTrue(formset.edit_only)
        
    def test_edit_only_defaults_false(self):
        """Test that edit_only defaults to False."""
        FormSet = modelformset_factory(
            Author, 
            fields=['name']
        )
        
        formset = FormSet()
        self.assertTrue(hasattr(formset, 'edit_only'))
        self.assertFalse(formset.edit_only)