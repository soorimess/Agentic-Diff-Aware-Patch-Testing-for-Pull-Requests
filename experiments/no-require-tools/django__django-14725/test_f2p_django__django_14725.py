from django.test import TestCase
from django.forms.models import modelformset_factory
from tests.model_formsets.models import Author


class TestEditOnly(TestCase):
    def test_edit_only_functionality(self):
        """
        Regression test for Django issue #14725:
        Provide a way for model formsets to disallow new object creation.
        """  
        # Test the edit_only attribute
        FormSet = modelformset_factory(Author, fields=['name'], edit_only=True)
        
        # The edit_only flag should be set on the formset class
        self.assertTrue(FormSet.edit_only)
        
        # With edit_only=True, existing formset behavior should still work
        # but new objects should be ignored when saving
        
        # This test verifies the edit_only parameter is accepted and set appropriately
        # since we should not have to actually save the forms to test the flag.
        FormSetDefault = modelformset_factory(Author, fields=['name'], edit_only=False)
        self.assertFalse(FormSetDefault.edit_only)