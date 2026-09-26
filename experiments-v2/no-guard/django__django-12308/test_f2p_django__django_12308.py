from django.contrib.admin.utils import display_for_field
from django.db import models
from django.test import TestCase


class JSONFieldDisplayTest(TestCase):
    def test_jsonfield_display_for_field_with_dict_value(self):
        """
        Test that JSONField values are properly displayed in admin when they are readonly.
        Before the fix, {"foo": "bar"} would be displayed as {'foo': 'bar'}, which is not valid JSON.
        """
        # Create a mock JSONField instance
        field = models.JSONField()
        
        # Test with a dictionary value
        value = {"foo": "bar"}
        
        # This should return valid JSON string representation, not a Python dict representation
        result = display_for_field(value, field, empty_value_display="-")
        
        # The result should be a JSON string representation, not a Python dict representation
        # Before the fix, this would return something like: {'foo': 'bar'} (Python dict repr)
        # After the fix, this should return: {"foo": "bar"} (valid JSON)
        self.assertEqual(result, '{"foo": "bar"}')
        
    def test_jsonfield_display_for_field_with_list_value(self):
        """
        Test that JSONField values with list are properly displayed.
        """
        field = models.JSONField()
        value = ["foo", "bar"]
        
        result = display_for_field(value, field, empty_value_display="-")
        
        # Should return valid JSON string representation
        self.assertEqual(result, '["foo", "bar"]')
        
    def test_jsonfield_display_for_field_with_string_value(self):
        """
        Test that JSONField values with string are properly displayed.
        """
        field = models.JSONField()
        value = "hello world"
        
        result = display_for_field(value, field, empty_value_display="-")
        
        # Should return valid JSON string representation
        self.assertEqual(result, '"hello world"')
        
    def test_jsonfield_display_for_field_with_none_value(self):
        """
        Test that JSONField handles None values properly.
        """
        field = models.JSONField()
        value = None
        
        result = display_for_field(value, field, empty_value_display="-")
        
        # Should return empty_value_display for None values
        self.assertEqual(result, "-")
        
    def test_jsonfield_display_for_field_with_invalid_json(self):
        """
        Test that JSONField handles invalid JSON properly (should fall back to display_for_value).
        """
        field = models.JSONField()
        # This would cause a TypeError in get_prep_value
        value = object()  # Non-serializable object
        
        result = display_for_field(value, field, empty_value_display="-")
        
        # Should fall back to display_for_value behavior
        # This depends on how display_for_value handles non-serializable objects
        # but should not raise an exception
        self.assertIsInstance(result, str)