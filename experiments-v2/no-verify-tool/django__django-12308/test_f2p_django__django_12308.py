import unittest
from django.contrib.admin.utils import display_for_field
from django.db import models


class JSONFieldAdminDisplayTest(unittest.TestCase):
    def test_jsonfield_display_in_admin(self):
        """Test that JSONField values are properly formatted in admin display."""
        # Create a JSONField instance
        field = models.JSONField()
        
        # Test with a simple dict value
        test_value = {"foo": "bar"}
        
        # This should return a valid JSON string, not a Python dict representation
        result = display_for_field(test_value, field, empty_value_display="-")
        
        # Before the fix, this would return something like {'foo': 'bar'} (Python dict repr)
        # After the fix, this should return {"foo": "bar"} (valid JSON string)
        # The key difference is that JSON should use double quotes, not single quotes
        self.assertEqual(result, '{"foo": "bar"}')
        
    def test_jsonfield_display_with_nested_dict(self):
        """Test that nested JSONField values are properly formatted."""
        field = models.JSONField()
        test_value = {"a": [1, 2, 3], "b": {"nested": "value"}}
        
        result = display_for_field(test_value, field, empty_value_display="-")
        
        # Should be valid JSON string
        self.assertEqual(result, '{"a": [1, 2, 3], "b": {"nested": "value"}}')
        
    def test_jsonfield_display_with_none(self):
        """Test that None values are handled correctly."""
        field = models.JSONField()
        test_value = None
        
        result = display_for_field(test_value, field, empty_value_display="-")
        
        # None should be handled by the empty_value_display logic
        self.assertEqual(result, "-")
        
    def test_jsonfield_display_with_string(self):
        """Test that string values are properly formatted."""
        field = models.JSONField()
        test_value = "simple string"
        
        result = display_for_field(test_value, field, empty_value_display="-")
        
        # Should be a JSON string representation
        self.assertEqual(result, '"simple string"')
        
    def test_jsonfield_display_with_number(self):
        """Test that numeric values are properly formatted."""
        field = models.JSONField()
        test_value = 42
        
        result = display_for_field(test_value, field, empty_value_display="-")
        
        # Should be a JSON number representation
        self.assertEqual(result, "42")