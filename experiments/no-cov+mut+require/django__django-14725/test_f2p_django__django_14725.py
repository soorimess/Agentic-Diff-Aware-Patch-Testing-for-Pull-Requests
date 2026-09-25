"""
Regression test for Django formset edit_only parameter.
Tests that the edit_only parameter now works correctly.
"""
from django.test import TestCase


class EditOnlyFormsetTest(TestCase):
    def test_edit_only_parameter_accepted_by_factory(self):
        """
        Test that modelformset_factory accepts edit_only parameter.
        This is the core API change that must be verified.
        """
        # This test should fail before the fix and pass after
        from django.forms.models import modelformset_factory
        
        # The API change: edit_only should be accepted as a parameter
        try:
            # This should work after the change and fail before
            FormSet = modelformset_factory(None, fields=[], edit_only=True)  
            self.assertTrue(True)  # If we get here, the parameter was accepted  
        except TypeError as e:
            if "unexpected keyword argument 'edit_only'" in str(e):
                # This means edit_only parameter is not yet supported - expected before fix
                self.fail("edit_only parameter not supported by modelformset_factory (API not updated)")
            else:
                # Some other error, re-raise since it's not related to our fix
                raise e