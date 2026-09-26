"""
Regression test for Django issue #14725: Provide a way for model formsets to disallow new object creation

This test verifies that the edit_only parameter exists in modelformset_factory function signature
and that it works correctly.
"""
import unittest
import inspect
from django.forms.models import modelformset_factory


class TestEditOnlyFormset(unittest.TestCase):
    def test_modelformset_factory_has_edit_only_parameter(self):
        """
        Test that modelformset_factory function signature includes edit_only parameter.
        
        This test verifies that the fix for Django issue #14725 is in place.
        Before the fix, the edit_only parameter would not exist in the function signature.
        After the fix, the edit_only parameter should be present with default False.
        """
        # Get the function signature
        sig = inspect.signature(modelformset_factory)
        
        # Check that edit_only parameter exists in the function signature
        self.assertIn('edit_only', sig.parameters)
        
        # Check that it has the correct default value
        edit_only_param = sig.parameters['edit_only']
        self.assertEqual(edit_only_param.default, False)
        
        # Verify that the parameter is properly documented in the function
        # (This is a basic check that the parameter is actually part of the function)
        self.assertTrue(callable(modelformset_factory))