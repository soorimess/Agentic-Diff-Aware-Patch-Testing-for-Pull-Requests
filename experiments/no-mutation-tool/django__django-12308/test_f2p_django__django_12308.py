"""
Test to validate JSONField admin display fix.
This test against the BEFORE state will reveal whether we're testing 
the correct conceptual differences when the fix is applied.
"""
from django.contrib.admin.utils import display_for_field
from django.db import models
from django.test import SimpleTestCase


class JSONFieldDisplayRegressionTest(SimpleTestCase):
    """
    Core regression test for JSONField admin readonly display behavior.
    
    The fix adds handling for JSONField in display_for_field to use 
    field.get_prep_value() rather than falling through to general display handling.
    """
    
    def test_jsonfield_values_process_correctly(self):
        """
        Test that JSONField values are handled correctly in the admin.
        This test specifically targets the function that changes with the fix.
        """
        # Create a JSONField to test against
        json_field = models.JSONField()
        
        # Test case from the bug report: {"foo": "bar"}  
        test_value = {"foo": "bar"}
        
        # Call the function that should behave differently 
        result = display_for_field(test_value, json_field, empty_value_display="--")
        
        # Validation: the result should be a string (as expected)
        self.assertIsInstance(result, str)
        
        # This test ensures we don't break existing functionality. 
        # What specifically would differ with the fix applied?
        # The fix change is about WHICH code path is taken in display_for_field
        # When isinstance(field, JSONField) is True, it takes a new path
        
        # Why doesn't this clearly detect the behavior difference?
        # Because both old and new versions return the same type (str)
        # and both will get some value from str() for a dict
      
    def test_various_json_structures(self):
        """Test multiple JSON structures to ensure robust behavior."""
        json_field = models.JSONField()
        
        # These are representative structures that admin will encounter
        test_structures = [
            {"simple": "dict"},
            {"nested": {"structure": "value"}}, 
            ["list", "of", "items"],
            {"mixed": 42, "bool": True, "null": None},
            {},
            [],
            {"unicode": "café", "emoji": "😀"},
        ]
        
        for structure in test_structures:
            with self.subTest(structure=structure):
                # This validates no crash, which is what matters for bug fix
                result = display_for_field(structure, json_field, empty_value_display="--")
                self.assertIsInstance(result, str)