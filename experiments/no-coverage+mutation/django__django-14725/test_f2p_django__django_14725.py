"""
Regression test for Django #14725: Model formsets to disallow new object creation
This test ensures that both modelformset_factory and inlineformset_factory
accept the edit_only parameter, which is the core change required to fix the bug.
"""
from django.test import TestCase

class TestFormsetEditOnlySignature(TestCase):
    def test_modelformset_factory_signature(self):
        """
        Test that modelformset_factory accepts edit_only parameter.
        Before fix: TypeError with "unexpected keyword argument"
        After fix: No longer gets that error
        """
        from django.forms.models import modelformset_factory

        # This specifically tests that edit_only parameter exists in signature 
        # by trying to pass it
        try:
            # If edit_only was not part of the signature, this would fail with
            # TypeError: modelformset_factory() got an unexpected keyword argument 'edit_only'
            modelformset_factory(object, fields=['id'], edit_only=True)
        except TypeError as e:
            error_msg = str(e)
            if "unexpected keyword argument" in error_msg and "edit_only" in error_msg:
                # This is the problem we are trying to fix - rejecting edit_only
                self.fail("edit_only parameter is not accepted by modelformset_factory")
            # Some other TypeError, let it pass through (different failure is fine)

    def test_inlineformset_factory_signature(self):
        """
        Test that inlineformset_factory accepts edit_only parameter.
        Before fix: TypeError with "unexpected keyword argument"
        After fix: No longer gets that error
        """
        from django.forms.models import inlineformset_factory

        # This specifically tests that edit_only parameter exists in signature  
        # by trying to pass it
        try:
            # If edit_only was not part of the signature, this would fail with
            # TypeError: inlineformset_factory() got an unexpected keyword argument 'edit_only'  
            inlineformset_factory(object, object, fields=['id'], edit_only=True)
        except TypeError as e:
            error_msg = str(e)
            if "unexpected keyword argument" in error_msg and "edit_only" in error_msg:
                # This is the problem we are trying to fix - rejecting edit_only
                self.fail("edit_only parameter is not accepted by inlineformset_factory")
            # Some other TypeError, let it pass through (different failure is fine)