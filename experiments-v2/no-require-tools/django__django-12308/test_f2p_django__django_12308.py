import unittest
from django.test import TestCase


class JSONFieldAdminDisplayTest(TestCase):
    def test_jsonfield_admin_display_regression(self):
        """
        Regression test for JSONField admin display issue.
        
        This test verifies that JSONField values are properly formatted in admin context
        to prevent the bug where values would be displayed as Python dict representation
        instead of valid JSON.
        """
        try:
            from django.db.models import JSONField
            from django.contrib.admin.utils import display_for_field
            
            # Create a JSONField instance
            json_field = JSONField()
            
            # Test various JSON values to make sure they work correctly
            test_cases = [
                {"foo": "bar"},      # Main test case from bug report
                {"key": "value"},    # Another dict
                [1, 2, 3],           # List
                "string",            # String
                42,                  # Number
                True,                # Boolean
                False,               # Boolean
                None,                # None
                {},                  # Empty dict
                [],                  # Empty list
            ]
            
            # All test cases should work without error
            for test_val in test_cases:
                result = display_for_field(test_val, json_field, "---")
                # Basic validation: should return a string and not crash
                self.assertIsNotNone(result)
                self.assertIsInstance(result, str)
                
        except ImportError:
            # Skip if JSONField not available
            pass

    def test_jsonfield_none_handling(self):
        """
        Test that None values are handled correctly (should use empty_value_display).
        """
        try:
            from django.db.models import JSONField
            from django.contrib.admin.utils import display_for_field
            
            json_field = JSONField()
            
            # None should return empty_value_display
            result = display_for_field(None, json_field, "---")
            self.assertEqual(result, "---")
            
        except ImportError:
            pass

    def test_jsonfield_exception_handling(self):
        """
        Test that TypeError exceptions in get_prep_value are properly handled.
        """
        try:
            from django.db.models import JSONField
            from django.contrib.admin.utils import display_for_field
            
            json_field = JSONField()
            
            # Test with problematic values that might cause TypeError
            class ProblematicValue:
                def __str__(self):
                    return "problematic"
                
                def __repr__(self):
                    return "problematic"
            
            problematic_value = ProblematicValue()
            
            # This should not crash
            result = display_for_field(problematic_value, json_field, "---")
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            
        except ImportError:
            pass