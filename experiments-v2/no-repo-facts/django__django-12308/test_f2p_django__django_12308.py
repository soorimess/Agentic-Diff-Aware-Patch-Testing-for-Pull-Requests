from django.contrib.admin.utils import display_for_field
from django.db import models
from django.test import TestCase
import json


class JSONFieldDisplayTest(TestCase):
    def test_jsonfield_display_for_field_returns_valid_json(self):
        """
        Test that JSONField values are properly displayed as valid JSON strings.
        
        The bug: JSONField values were displayed as Python dict representation
        with single quotes, which is not valid JSON.
        
        Example: {"foo": "bar"} would be displayed as {'foo': 'bar'} (invalid JSON)
        Instead of: {"foo": "bar"} (valid JSON)
        """
        # Create a mock JSONField that mimics the real JSONField behavior
        class MockJSONField(models.JSONField):
            def __init__(self):
                super().__init__()
            
            def get_prep_value(self, value):
                # This mimics the actual JSONField.get_prep_value behavior
                if value is None:
                    return value
                return json.dumps(value, cls=self.encoder)
        
        # Test data that demonstrates the bug
        test_value = {"foo": "bar", "number": 42}
        empty_value_display = "-"

        # Create a JSONField instance
        json_field = MockJSONField()
        
        # Test the display_for_field function
        result = display_for_field(test_value, json_field, empty_value_display)
        
        # The result should be valid JSON with double quotes
        self.assertIsInstance(result, str)
        
        # Should be able to parse as JSON (valid JSON)
        parsed = json.loads(result)
        self.assertEqual(parsed, test_value)
        
        # Should contain double quotes (valid JSON format)  
        self.assertIn('"foo"', result)
        # Should NOT contain single quotes in the JSON structure
        self.assertNotIn("'foo'", result)

    def test_jsonfield_display_for_field_handles_invalid_values(self):
        """
        Test that JSONField gracefully handles invalid values that would cause
        TypeError in get_prep_value, falling back to display_for_value.
        """
        class MockJSONField(models.JSONField):
            def __init__(self):
                super().__init__()
            
            def get_prep_value(self, value):
                # This will raise TypeError for invalid values like objects
                if value is None:
                    return value
                return json.dumps(value, cls=self.encoder)
        
        # Test with an invalid JSON value that would raise TypeError
        invalid_value = object()  # This would cause TypeError in json.dumps
        empty_value_display = "-"

        # Create a JSONField instance
        json_field = MockJSONField()
        
        # Test the display_for_field function - should fall back gracefully
        result = display_for_field(invalid_value, json_field, empty_value_display)
        
        # Should return the empty_value_display when get_prep_value raises TypeError
        # (this is the fallback behavior that should work both before and after fix)
        self.assertEqual(result, empty_value_display)