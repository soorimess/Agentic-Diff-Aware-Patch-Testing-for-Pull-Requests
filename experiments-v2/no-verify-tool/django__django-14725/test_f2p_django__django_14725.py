"""
Regression test for Django issue #14725:
Provide a way for model formsets to disallow new object creation.

This test verifies that the edit_only parameter is properly implemented
in modelformset_factory and inlineformset_factory functions.
"""

from django.db import models
from django.forms.models import modelformset_factory, inlineformset_factory
from django.test import TestCase


class ModelFormsetEditOnlyParameterTests(TestCase):
    """Tests that the edit_only parameter is accepted by formset factories."""

    def test_modelformset_factory_accepts_edit_only_parameter(self):
        """Test that modelformset_factory accepts edit_only parameter."""
        # Using a simple model for testing
        class TestModel(models.Model):
            name = models.CharField(max_length=100)
            
            class Meta:
                app_label = 'test'
        
        # This should not raise a TypeError
        FormSet = modelformset_factory(TestModel, fields=['name'], edit_only=True)
        self.assertTrue(hasattr(FormSet, 'edit_only'))
        self.assertTrue(FormSet.edit_only)

    def test_inlineformset_factory_accepts_edit_only_parameter(self):
        """Test that inlineformset_factory accepts edit_only parameter."""
        # Using simple models for testing
        class ParentModel(models.Model):
            name = models.CharField(max_length=100)
            
            class Meta:
                app_label = 'test'
                
        class ChildModel(models.Model):
            name = models.CharField(max_length=100)
            parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)
            
            class Meta:
                app_label = 'test'
        
        # This should not raise a TypeError
        FormSet = inlineformset_factory(ParentModel, ChildModel, fields=['name'], edit_only=True)
        self.assertTrue(hasattr(FormSet, 'edit_only'))
        self.assertTrue(FormSet.edit_only)


# The actual behavior tests will be implemented once the functionality is available
# They would test:
# 1. When edit_only=True, new objects are not created
# 2. When edit_only=True, existing objects are still saved
# 3. When edit_only=False (default), both new and existing objects are handled