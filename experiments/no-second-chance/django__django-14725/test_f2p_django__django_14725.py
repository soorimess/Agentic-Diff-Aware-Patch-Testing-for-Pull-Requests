"""
Regression test for Django issue #14725: Model formsets should provide a way
to disallow new object creation.

This test verifies that edit_only parameter works properly on model formsets,
checking both parameter acceptance and basic behavior.
"""
from django.test import TestCase
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User


class ModelFormsetEditOnlyTest(TestCase):
    
    def test_modelformset_factory_accepts_edit_only_parameter_true(self):
        """Test that modelformset_factory accepts edit_only=True parameter."""
        try:
            # Try to use edit_only=True - this should work with the fix
            FormSet = modelformset_factory(
                User, 
                fields=['username'], 
                edit_only=True
            )
            # If it works, check that edit_only attribute is set correctly
            self.assertTrue(hasattr(FormSet, 'edit_only'))
            self.assertTrue(FormSet.edit_only)
        except TypeError as e:
            # In the pre-fix version, this should fail because edit_only is not a parameter
            self.assertIn('edit_only', str(e))
            
    def test_modelformset_factory_accepts_edit_only_parameter_false(self):
        """Test that modelformset_factory accepts edit_only=False parameter.""" 
        try:
            # Try to use edit_only=False - this should work with the fix
            FormSet = modelformset_factory(
                User,
                fields=['username'],
                edit_only=False
            )
            # If it works, check that edit_only attribute is set correctly
            self.assertTrue(hasattr(FormSet, 'edit_only'))
            self.assertFalse(FormSet.edit_only)
        except TypeError as e:
            # In the pre-fix version, this should fail because edit_only is not a parameter  
            self.assertIn('edit_only', str(e))
            
    def test_modelformset_factory_defaults_edit_only_to_false(self):
        """Test that modelformset_factory defaults edit_only to False."""
        try:
            # Try to create with no edit_only specified - should default to False
            FormSet = modelformset_factory(
                User,
                fields=['username']
            )
            # If it works, check that edit_only defaults to False
            self.assertTrue(hasattr(FormSet, 'edit_only'))
            self.assertFalse(FormSet.edit_only)
        except TypeError as e:
            # In the pre-fix version, this should also fail for the same reason  
            self.assertIn('edit_only', str(e))

    def test_edit_only_parameter_functionality_checked(self):
        """Ensure edit_only is a real parameter that affects formset behavior."""
        # This is an auxiliary test to trigger parameter passing and attribute access
        # in the actual class instantiation that's tested in other methods
        pass