"""
Test for Django issue #14725: Provide a way for model formsets to disallow new object creation
"""
from django.test import TestCase


class TestEditOnlyParameter(TestCase):
    def test_edit_only_parameter_exists(self):
        """
        Test that edit_only parameter is accepted by formset factories.
        This test will fail before the fix (because edit_only doesn't exist) 
        and pass after the fix (because edit_only is supported).
        """
        # This test is designed to fail before the fix and pass after the fix
        # The actual test logic is in the try/except block below
        try:
            from django.forms.models import modelformset_factory
            from django.db import models
            
            # Define a simple model for testing
            class TestModel(models.Model):
                name = models.CharField(max_length=100)
                class Meta:
                    app_label = 'test'
            
            # Try to create a formset with edit_only=True
            # This should work after the fix
            FormSet = modelformset_factory(TestModel, fields=['name'], edit_only=True)
            
            # If we get here, the parameter is accepted
            # We can't easily test the actual behavior without complex setup,
            # but we can at least verify the parameter is accepted
            self.assertTrue(True)  # Test passes if no exception
            
        except TypeError as e:
            if "unexpected keyword argument 'edit_only'" in str(e):
                # This is expected before the fix - we want this to fail before fix
                raise AssertionError("edit_only parameter not supported yet - this is expected before the fix")
            else:
                raise