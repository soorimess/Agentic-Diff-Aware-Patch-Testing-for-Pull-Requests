from django.contrib.admin.utils import display_for_field
from django.db import models
from django.test import TestCase


class JSONFieldDisplayTest(TestCase):
    def test_jsonfield_display_in_admin_before_fix(self):
        """
        Test that demonstrates the bug: JSONField values are displayed as 
        Python dict representation instead of valid JSON when using display_for_field.
        This test should fail before the fix and pass after the fix.
        """
        # Create a mock JSONField instance
        json_field = models.JSONField()
        
        # Test data - a dict that would be displayed in admin
        test_value = {"foo": "bar", "number": 42}
        
        # This should return valid JSON format (double quotes) not Python dict format (single quotes)
        result = display_for_field(test_value, json_field, empty_value_display="")
        
        # The key assertion: result should be valid JSON format with double quotes
        # Before fix: would show something like {'foo': 'bar', 'number': 42} (single quotes)
        # After fix: should show something like {"foo": "bar", "number": 42} (double quotes)
        self.assertIsInstance(result, str)
        
        # Check that it uses double quotes (valid JSON) rather than single quotes (Python dict)
        # The fix ensures that JSONField values go through get_prep_value which returns proper JSON
        self.assertIn('"foo"', result)  # Should have double quotes (valid JSON)
        self.assertNotIn("'foo'", result)  # Should not have single quotes (Python dict)
        
    def test_jsonfield_with_none_value(self):
        """
        Test that JSONField with None value is handled correctly.
        """
        json_field = models.JSONField()
        result = display_for_field(None, json_field, empty_value_display="N/A")
        self.assertEqual(result, "N/A")
        
    def test_jsonfield_with_complex_structure(self):
        """
        Test JSONField with more complex nested structure.
        """
        json_field = models.JSONField()
        test_value = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ],
            "total": 2
        }
        result = display_for_field(test_value, json_field, empty_value_display="")
        
        # Should be valid JSON with double quotes
        self.assertIsInstance(result, str)
        self.assertIn('"users"', result)
        self.assertIn('"Alice"', result)
        self.assertNotIn("'Alice'", result)
        
    def test_jsonfield_with_invalid_value_raises_typeerror(self):
        """
        Test that JSONField handles TypeError gracefully when get_prep_value fails.
        """
        # Create a JSONField instance
        json_field = models.JSONField()
        
        # Create an object that can't be serialized to JSON
        class InvalidObject:
            def __init__(self):
                self.value = 42
        
        invalid_obj = InvalidObject()
        
        # This should fall back to display_for_value behavior when TypeError occurs
        result = display_for_field(invalid_obj, json_field, empty_value_display="N/A")
        
        # Should fall back to the default behavior (likely str() representation)
        self.assertIsInstance(result, str)
        # The exact behavior depends on display_for_value, but it shouldn't crash