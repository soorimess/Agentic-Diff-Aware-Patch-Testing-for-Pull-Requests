"""
Regression test for JSONField admin display issue.
Tests that ensure JSONField values are displayed properly in Django admin.
"""

from django.contrib.admin.utils import display_for_field
from django.db import models
from django.test import TestCase


class TestJSONFieldAdminDisplay(TestCase):
    def test_jsonfield_display_for_field_with_mock_jsonfield(self):
        """
        Test JSONField admin display behavior.
        
        Before fix: JSONField values would be processed through generic display_for_value
        which would return string representation with single quotes: {'foo': 'bar'}
        
        After fix: JSONField values should use get_prep_value() for proper formatting
        resulting in JSON string: {"foo": "bar"}
        """
        
        # Create a mock field that behaves like JSONField
        class MockJSONField(models.Field):
            def get_prep_value(self, value):
                # Simulate what get_prep_value does for JSONField
                import json
                if value is None:
                    return value
                return json.dumps(value)
        
        field = MockJSONField()
        test_value = {"foo": "bar"}
        
        # Call the function under test
        result = display_for_field(test_value, field, empty_value_display='---')
        
        # Verify it returns a string (ensures no exception)
        self.assertIsInstance(result, str)
        
        # Most importantly, ensure it doesn't return the buggy single-quote format
        self.assertNotEqual(result, "{'foo': 'bar'}")