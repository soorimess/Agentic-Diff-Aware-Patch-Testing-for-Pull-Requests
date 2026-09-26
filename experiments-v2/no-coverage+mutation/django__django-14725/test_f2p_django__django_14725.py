from django.db import models
from django.forms.models import modelformset_factory
from django.test import TestCase

# Create simple models for testing
class Author(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'test'

class EditOnlyFormsetTest(TestCase):
    def test_edit_only_parameter_exists_in_modelformset_factory(self):
        """
        Test that modelformset_factory accepts edit_only parameter.
        This test will fail before the fix and pass after the fix.
        """
        # This test verifies that the edit_only parameter can be passed
        # and that the FormSet gets the edit_only attribute set correctly
        try:
            FormSet = modelformset_factory(
                Author, 
                fields=['name'], 
                edit_only=True
            )
            
            # After the fix, this should work and the FormSet should have edit_only attribute
            self.assertTrue(hasattr(FormSet, 'edit_only'))
            self.assertTrue(FormSet.edit_only)
            
        except TypeError as e:
            # Before the fix, this will fail with "unexpected keyword argument 'edit_only'"
            if "unexpected keyword argument 'edit_only'" in str(e):
                # This is expected before the fix - we want this to fail
                # so that when the fix is applied, this test will pass
                raise AssertionError("edit_only parameter not supported - fix needed")
            else:
                raise e

    def test_edit_only_parameter_default_false(self):
        """
        Test that edit_only parameter defaults to False.
        This test will fail before the fix and pass after the fix.
        """
        try:
            FormSet = modelformset_factory(
                Author, 
                fields=['name']
            )
            
            # After the fix, this should work and the FormSet should have edit_only attribute
            self.assertTrue(hasattr(FormSet, 'edit_only'))
            self.assertFalse(FormSet.edit_only)
            
        except TypeError as e:
            # Before the fix, this will fail with "unexpected keyword argument 'edit_only'"
            if "unexpected keyword argument 'edit_only'" in str(e):
                # This is expected before the fix
                raise AssertionError("edit_only parameter not supported - fix needed")
            else:
                raise e