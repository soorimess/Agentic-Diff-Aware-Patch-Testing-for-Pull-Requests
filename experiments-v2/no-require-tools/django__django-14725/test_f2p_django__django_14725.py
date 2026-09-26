from django.test import TestCase

class EditOnlyFormsetTest(TestCase):
    def test_edit_only_parameter_exists_in_signatures(self):
        """
        Test that edit_only parameter exists in function signatures.
        This verifies that the API has been updated to accept edit_only parameter.
        """
        # Import the functions to check their signatures
        from django.forms.models import modelformset_factory, inlineformset_factory
        
        # Check that the functions accept edit_only parameter
        import inspect
        
        # Get the function signatures
        modelformset_sig = inspect.signature(modelformset_factory)
        inlineformset_sig = inspect.signature(inlineformset_factory)
        
        # Verify that edit_only is in the parameters
        self.assertIn('edit_only', modelformset_sig.parameters)
        self.assertIn('edit_only', inlineformset_sig.parameters)
        
        # Verify default value is False
        self.assertEqual(modelformset_sig.parameters['edit_only'].default, False)
        self.assertEqual(inlineformset_sig.parameters['edit_only'].default, False)