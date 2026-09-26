from django.test import TestCase

class EditOnlyFormsetTests(TestCase):
    
    def test_edit_only_parameter_in_modelformset_factory_signature(self):
        """
        Test that the edit_only parameter exists in modelformset_factory function signature.
        This test will fail before the fix and pass after the fix.
        """
        import inspect
        from django.forms.models import modelformset_factory
        
        # Get the function signature
        sig = inspect.signature(modelformset_factory)
        params = list(sig.parameters.keys())
        
        # Check if 'edit_only' is in the parameters
        # This should be true after the fix
        if 'edit_only' in params:
            # Parameter exists - this is the new behavior
            self.assertTrue(True)  # Test passes
        else:
            # Parameter doesn't exist - this is the old behavior
            raise AssertionError("edit_only parameter not found in modelformset_factory signature - this indicates the old behavior")
    
    def test_edit_only_parameter_in_inlineformset_factory_signature(self):
        """
        Test that the edit_only parameter exists in inlineformset_factory function signature.
        This test will fail before the fix and pass after the fix.
        """
        import inspect
        from django.forms.models import inlineformset_factory
        
        # Get the function signature
        sig = inspect.signature(inlineformset_factory)
        params = list(sig.parameters.keys())
        
        # Check if 'edit_only' is in the parameters
        # This should be true after the fix
        if 'edit_only' in params:
            # Parameter exists - this is the new behavior
            self.assertTrue(True)  # Test passes
        else:
            # Parameter doesn't exist - this is the old behavior
            raise AssertionError("edit_only parameter not found in inlineformset_factory signature - this indicates the old behavior")