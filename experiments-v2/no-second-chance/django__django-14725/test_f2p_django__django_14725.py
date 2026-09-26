from django.test import TestCase


class ModelFormsetEditOnlyTests(TestCase):
    """Tests for the edit_only functionality in model formsets."""

    def test_modelformset_factory_accepts_edit_only_parameter(self):
        """Test that modelformset_factory accepts edit_only parameter."""
        # This test verifies the API change introduced by the fix
        # Before fix: TypeError with "unexpected keyword argument 'edit_only'"
        # After fix: Should work without that specific error
        from django.forms.models import modelformset_factory
        
        # If this raises TypeError with "unexpected keyword argument", 
        # the fix hasn't been applied yet
        try:
            modelformset_factory(None, fields=[], edit_only=True)
        except TypeError as e:
            if "unexpected keyword argument 'edit_only'" in str(e):
                # This is the specific error we expect before the fix
                # The test should fail with this error to indicate fix not applied
                raise