from django.contrib.admin.utils import display_for_field
from django.db import models
from django.test import TestCase


class TestJSONFieldDisplay(TestCase):
    def test_jsonfield_display_in_admin(self):
        """Test that JSONField values are properly formatted in admin display."""
        # Create a mock JSONField instance
        json_field = models.JSONField()
        
        # Test with a simple dict - this is the main bug case
        test_value = {"foo": "bar"}
        
        # This should return valid JSON format, not Python dict representation
        result = display_for_field(test_value, json_field, empty_value_display="")
        
        # The bug: before fix, it returns {'foo': 'bar'} (Python dict repr with single quotes)
        # The fix: after fix, it should return proper JSON format like {"foo": "bar"} 
        # The key assertion: result should NOT be the problematic Python dict representation
        self.assertNotEqual(result, "{'foo': 'bar'}")