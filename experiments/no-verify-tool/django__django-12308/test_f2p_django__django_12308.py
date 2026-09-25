"""
Regression test for Django JSONField admin display issue.
Tests that JSONField values are properly formatted as JSON strings instead 
of Python dictionary representations when displayed in admin.
"""
from django.test import TestCase
from django.db import models
from django.contrib.admin.utils import display_for_field


class JSONFieldAdminDisplayTest(TestCase):
    def test_jsonfield_display_format(self):
        """
        Test that JSONField values are properly formatted for admin display.
        
        Before the fix: JSONField values like {"foo": "bar"} would be displayed 
        as {'foo': 'bar'} (Python dict representation)
        
        After the fix: JSONField values should be displayed as {"foo": "bar"} 
        (valid JSON format)
        """
        # Create a JSONField instance
        json_field = models.JSONField()
        
        # Test simple dictionary
        value = {"foo": "bar"}
        result = display_for_field(value, json_field, "--")
        
        # This should be valid JSON (after fix)
        # The key assertion - this requires proper JSON serialization
        expected = '{"foo": "bar"}'
        self.assertEqual(result, expected)
        
        # Test nested structure
        nested_value = {"nested": {"key": "value"}, "array": [1, 2, 3]}
        result = display_for_field(nested_value, json_field, "--")
        expected = '{"nested": {"key": "value"}, "array": [1, 2, 3]}'
        self.assertEqual(result, expected)
        
        # Test empty dict
        empty_value = {}
        result = display_for_field(empty_value, json_field, "--")
        expected = '{}'
        self.assertEqual(result, expected)
        
    def test_jsonfield_none_handling(self):
        """Test that None values work correctly."""
        json_field = models.JSONField()
        result = display_for_field(None, json_field, "--")
        self.assertEqual(result, "--")
        
    def test_jsonfield_various_types(self):
        """Test JSONField with various data types."""
        json_field = models.JSONField()
        
        # Test string
        result = display_for_field("test string", json_field, "--")
        expected = '"test string"'
        self.assertEqual(result, expected)
        
        # Test number
        result = display_for_field(123, json_field, "--")
        expected = '123'
        self.assertEqual(result, expected)
        
        # Test boolean  
        result = display_for_field(True, json_field, "--")
        expected = 'true'
        self.assertEqual(result, expected)