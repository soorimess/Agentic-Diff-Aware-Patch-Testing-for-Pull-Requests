import json
from django.contrib.admin.utils import display_for_field
from django.db import models
from django.test import TestCase


class TestJSONFieldDisplay(TestCase):
    def test_jsonfield_display_for_field_with_dict_value(self):
        """Test that JSONField values are properly formatted when displayed in admin."""
        # Create a mock JSONField instance
        class MockJSONField(models.JSONField):
            def __init__(self):
                super().__init__()
        
        field = MockJSONField()
        value = {"foo": "bar"}
        empty_value_display = "-"

        # Before the fix, this would return a dict representation like {'foo': 'bar'}
        # After the fix, this should return valid JSON like '{"foo": "bar"}'
        result = display_for_field(value, field, empty_value_display)
        
        # The result should be valid JSON string, not a dict representation
        # This is the key assertion that catches the bug
        self.assertIsInstance(result, str)
        
        # Try to parse it as JSON to verify it's valid
        try:
            parsed = json.loads(result)
            self.assertEqual(parsed, value)
        except json.JSONDecodeError:
            self.fail(f"Result '{result}' is not valid JSON")

    def test_jsonfield_display_for_field_with_list_value(self):
        """Test that JSONField with list values are properly formatted."""
        class MockJSONField(models.JSONField):
            def __init__(self):
                super().__init__()
        
        field = MockJSONField()
        value = ["foo", "bar", 123]
        empty_value_display = "-"

        result = display_for_field(value, field, empty_value_display)
        
        # The result should be valid JSON string
        self.assertIsInstance(result, str)
        
        # Try to parse it as JSON to verify it's valid
        try:
            parsed = json.loads(result)
            self.assertEqual(parsed, value)
        except json.JSONDecodeError:
            self.fail(f"Result '{result}' is not valid JSON")

    def test_jsonfield_display_for_field_with_none_value(self):
        """Test that JSONField with None values works correctly."""
        class MockJSONField(models.JSONField):
            def __init__(self):
                super().__init__()
        
        field = MockJSONField()
        value = None
        empty_value_display = "-"

        result = display_for_field(value, field, empty_value_display)
        
        # Should return the empty_value_display for None values
        self.assertEqual(result, "-")

    def test_jsonfield_display_for_field_with_unserializable_value(self):
        """Test that JSONField handles unserializable values gracefully."""
        class MockJSONField(models.JSONField):
            def __init__(self):
                super().__init__()
        
        field = MockJSONField()
        # This should cause a TypeError in json.dumps
        value = object()  # An object that can't be serialized to JSON
        empty_value_display = "-"

        # This should fall back to display_for_value when get_prep_value raises TypeError
        result = display_for_field(value, field, empty_value_display)
        
        # Should fall back to the default behavior for unserializable values
        self.assertIsInstance(result, str)
        # The result should be the string representation of the object
        self.assertIn("object", result)