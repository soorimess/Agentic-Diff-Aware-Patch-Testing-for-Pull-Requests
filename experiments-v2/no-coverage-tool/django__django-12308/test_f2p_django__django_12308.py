from django.contrib.admin.utils import display_for_field
from django.db import models
from django.test import TestCase


class JSONFieldTest(TestCase):
    def test_jsonfield_display_for_field(self):
        """
        Test that JSONField values are properly formatted when displayed in admin.
        Before the fix, JSONField values were displayed as Python dict representation
        instead of valid JSON strings.
        """
        # Create a mock JSONField instance
        class MockJSONField(models.JSONField):
            def __init__(self):
                super().__init__()
        
        field = MockJSONField()
        
        # Test case: Simple dict value
        value = {"foo": "bar"}
        empty_value_display = "-"
        
        # This should return a valid JSON string, not a Python dict representation
        result = display_for_field(value, field, empty_value_display)
        
        # Before the fix, this would return something like: "{'foo': 'bar'}" 
        # After the fix, this should return: '{"foo": "bar"}'
        self.assertEqual(result, '{"foo": "bar"}')
        
    def test_jsonfield_only_applied_to_jsonfields(self):
        """
        Test that the JSONField handling is only applied to JSONFields,
        not to other field types.
        """
        # Create a regular field to make sure our fix doesn't affect other fields
        class MockCharField(models.CharField):
            def __init__(self):
                super().__init__(max_length=100)
        
        field = MockCharField()
        value = {"foo": "bar"}
        empty_value_display = "-"
        
        # For non-JSONField, it should go through the normal path and not use get_prep_value
        # This test ensures we don't accidentally break other field types
        result = display_for_field(value, field, empty_value_display)
        # The result should be the Python representation of the dict, not JSON
        # This is the old behavior for non-JSONFields
        self.assertEqual(result, "{'foo': 'bar'}")