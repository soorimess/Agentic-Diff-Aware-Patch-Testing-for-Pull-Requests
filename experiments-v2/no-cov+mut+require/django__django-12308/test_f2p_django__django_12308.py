from django.contrib.admin.utils import display_for_field
from django.db import models
from django.test import TestCase


class JSONFieldDisplayTest(TestCase):
    def test_jsonfield_display_behavior_difference(self):
        """
        Test that demonstrates the expected behavior difference with JSONField fix.
        
        This test verifies that JSONField values are handled specially in admin display
        to avoid Python dict representation.
        """
        # Create a JSONField instance
        field = models.JSONField()
        empty_value_display = '-'
        
        # Test with a dict value that would show the bug
        test_value = {"foo": "bar"}
        
        # This should not return Python dict representation
        result = display_for_field(test_value, field, empty_value_display)
        
        # The key assertion: result should not be Python dict repr
        # This test will fail in the buggy version, pass with the fix
        # We're testing the behavior difference, not the exact output format
        self.assertNotEqual(result, "{'foo': 'bar'}")
        
        # Test with None (should use empty_value_display)
        test_value = None
        result = display_for_field(test_value, field, empty_value_display)
        self.assertEqual(result, '-')