from django.contrib.admin.utils import display_for_field
from django.contrib.admin.utils import display_for_value
from django.db import models
from django.test import TestCase
import json


class JSONFieldDisplayTest(TestCase):
    def test_jsonfield_display_for_field_with_dict(self):
        """Test that JSONField values are properly displayed in admin - the main bug."""
        # Create a mock JSONField instance
        class MockJSONField(models.JSONField):
            def __init__(self):
                super().__init__()
        
        field = MockJSONField()
        
        # Test with a simple dict - this is where the bug manifests
        test_value = {"foo": "bar"}
        
        # Before fix: this would fall through to display_for_value and return str(dict)
        # After fix: this should return valid JSON string
        result = display_for_field(test_value, field, empty_value_display="-")
        
        # Check that we get a string back
        self.assertIsInstance(result, str)
        
        # Verify it's valid JSON (this would fail before the fix)
        try:
            parsed = json.loads(result)
            self.assertEqual(parsed, test_value)
        except json.JSONDecodeError:
            # If it's not valid JSON, it's the bug - the old behavior
            self.fail("Result is not valid JSON - this indicates the bug is present")
    
    def test_jsonfield_display_for_field_with_nested_dict(self):
        """Test with nested dict structure."""
        class MockJSONField(models.JSONField):
            def __init__(self):
                super().__init__()
        
        field = MockJSONField()
        
        nested_value = {"a": [1, 2, 3], "b": {"nested": "value"}}
        result = display_for_field(nested_value, field, empty_value_display="-")
        
        self.assertIsInstance(result, str)
        
        # Verify it's valid JSON
        try:
            parsed = json.loads(result)
            self.assertEqual(parsed, nested_value)
        except json.JSONDecodeError:
            self.fail("Result is not valid JSON - this indicates the bug is present")
    
    def test_jsonfield_display_for_field_with_none(self):
        """Test that None values still work correctly."""
        class MockJSONField(models.JSONField):
            def __init__(self):
                super().__init__()
        
        field = MockJSONField()
        
        result = display_for_field(None, field, empty_value_display="-")
        self.assertEqual(result, "-")
    
    def test_jsonfield_display_for_field_with_empty_dict(self):
        """Test with empty dict."""
        class MockJSONField(models.JSONField):
            def __init__(self):
                super().__init__()
        
        field = MockJSONField()
        
        empty_dict = {}
        result = display_for_field(empty_dict, field, empty_value_display="-")
        
        self.assertIsInstance(result, str)
        
        # Verify it's valid JSON
        try:
            parsed = json.loads(result)
            self.assertEqual(parsed, empty_dict)
        except json.JSONDecodeError:
            self.fail("Result is not valid JSON - this indicates the bug is present")
            
    def test_jsonfield_display_for_field_with_list(self):
        """Test with list values."""
        class MockJSONField(models.JSONField):
            def __init__(self):
                super().__init__()
        
        field = MockJSONField()
        
        test_list = [1, 2, 3, "hello"]
        result = display_for_field(test_list, field, empty_value_display="-")
        
        self.assertIsInstance(result, str)
        
        # Verify it's valid JSON
        try:
            parsed = json.loads(result)
            self.assertEqual(parsed, test_list)
        except json.JSONDecodeError:
            self.fail("Result is not valid JSON - this indicates the bug is present")
            
    def test_jsonfield_display_for_field_with_typeerror_fallback(self):
        """Test that JSONField gracefully handles TypeError in get_prep_value."""
        # Create a JSONField that raises TypeError when get_prep_value is called
        class MockJSONFieldWithTypeError(models.JSONField):
            def __init__(self):
                super().__init__()
                
            def get_prep_value(self, value):
                # Simulate a case where get_prep_value raises TypeError
                # This could happen if json.dumps can't serialize the value
                if value == "invalid":
                    raise TypeError("Cannot serialize this object")
                return super().get_prep_value(value)
        
        field = MockJSONFieldWithTypeError()
        
        # Test with a value that causes TypeError in get_prep_value
        # This should fall back to display_for_value behavior
        result = display_for_field("invalid", field, empty_value_display="-")
        
        # Should fall back to display_for_value behavior which returns the string representation
        self.assertEqual(result, "invalid")