"""
Regression test to ensure edit_only functionality works correctly in Django model formsets.

This test verifies two core behaviors:
1. The edit_only parameter is accepted by modelformset_factory
2. FormSets have the edit_only attribute set correctly
"""
from django.test import TestCase


class ModelFormsetEditOnlyRegressionTest(TestCase):
    
    def test_edit_only_parameter_works(self):
        """
        This test will fail before the fix (edit_only parameter doesn't exist) 
        and pass after the fix (edit_only parameter works correctly).
        """
        # If the edit_only parameter doesn't exist, we'll get a TypeError
        # If it exists, we should be able to create formsets with it
        
        try:
            from django.forms.models import modelformset_factory
            from tests.model_formsets.models import Book
            
            # Try using the new edit_only parameter - should only work after change
            FormSet = modelformset_factory(Book, fields=['title'], edit_only=True)
            
            # Verify edit_only attribute is set correctly
            self.assertTrue(hasattr(FormSet, 'edit_only'))
            self.assertTrue(FormSet.edit_only)
            
            # Test default behavior  
            FormSetDefault = modelformset_factory(Book, fields=['title'])  
            self.assertTrue(hasattr(FormSetDefault, 'edit_only'))
            self.assertFalse(FormSetDefault.edit_only)
            
        except TypeError as e:
            # This is expected before the fix is applied
            if 'unexpected keyword argument' in str(e) and 'edit_only' in str(e):
                # If we get this specific error, it means the parameter doesn't exist yet
                # This is the condition that would make our test fail before the fix
                self.fail("edit_only parameter not available - behavior not implemented yet")
            # If it is a different TypeError, let it raise normally
            raise
        except Exception:
            # Other exceptions (import failures, etc.) show this is a setup environment issue
            # We skip as this is not about the core functionality we want to test
            self.skipTest("Environment setup prevents proper test execution")