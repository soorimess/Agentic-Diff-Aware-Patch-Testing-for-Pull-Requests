"""
Regression test for JSONField admin readonly display bug.

Before the fix, JSONField values showed as Python dict representations 
instead of valid JSON strings.
"""
from django.test import SimpleTestCase
from django.contrib.admin.utils import display_for_field
from django.db import models
import json


class JSONFieldAdminDisplayTest(SimpleTestCase):
    def test_jsonfield_admin_display_is_valid_json(self):
        """
        JSONField values in admin readonly displays should be valid JSON,
        not Python dict representations.
        
        This tests that the fix for the ticket properly formats JSONField
        values in the admin interface.
        """
        # Mock the behavior that should be achieved with field.get_prep_value
        class MockJSONField(models.Field):
            def get_prep_value(self, value):
                # This is the behavior we want - return valid JSON string
                if value is None:
                    return None
                return json.dumps(value, ensure_ascii=False)
                
        # Test data that would trigger the issue
        test_value = {"foo": "bar"}
        json_field = MockJSONField()
        
        # If the fix is NOT applied, this would use the generic display_for_value path
        # which gives Python dict representation, not valid JSON 
        result = display_for_field(test_value, json_field, "---")
        
        # The fix should make this behavior correct:
        # 1. Valid JSON string returned instead of Python repr
        # 2. Can be parsed back into identical structure
        
        self.assertIsInstance(result, str)
        
        try:
            # This should succeed with the fix applied 
            parsed = json.loads(result)
            self.assertEqual(parsed, test_value)
        except json.JSONDecodeError:
            # This means the old bug behavior where we got Python repr 
            self.fail("Expected valid JSON string but got Python representation: %s" % repr(result))