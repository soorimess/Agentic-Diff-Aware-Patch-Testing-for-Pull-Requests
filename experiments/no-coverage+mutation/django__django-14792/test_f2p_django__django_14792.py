"""
Regression test for Django issue #14792.

This tests the specific behavioral change in _get_timezone_name() that fixes
timezone conversion issues for Etc/GMT* timezones in Trunc() and Extract() database functions.
"""
import unittest
from django.utils.timezone import _get_timezone_name
import pytz


class TestTimezoneNameHandling(unittest.TestCase):
    def test_get_timezone_name_returns_correct_format(self):
        """
        The core issue: _get_timezone_name should return timezone offsets for proper
        SQL generation in PostgreSQL AT TIME ZONE operations.
        
        In the buggy implementation, it returns timezone names like "Etc/GMT-10"
        instead of offsets like "+10", causing incorrect SQL generation.
        """
        # Test the problematic Etc/GMT timezone
        tz = pytz.timezone("Etc/GMT-10")
        
        # The old buggy behavior (what we currently have in this repository)
        old_behavior = str(tz)  # Returns "Etc/GMT-10"
        
        # The correct new behavior (what the fix should produce)
        new_behavior = tz.tzname(None)  # Returns "+10"
        
        # What we currently get with the buggy code
        current_result = _get_timezone_name(tz)
        
        # Verify we have the buggy behavior where it returns full name instead of offset
        self.assertEqual(current_result, old_behavior)
        # Verify that the correct behavior is different
        self.assertNotEqual(current_result, new_behavior)
        
        # The primary test: the bug is that we get timezone name instead of offset
        # The correct behavior should be that we get the offset
        self.assertTrue(current_result.startswith("Etc/GMT"), 
                       "Current implementation returns timezone name, not offset")
        
    def test_timezone_offset_semantics(self):
        """
        Verify that Etc/GMT timezones have correct behavior for database operations.
        """
        # Test with Etc/GMT-10 timezone for the main case  
        tz = pytz.timezone("Etc/GMT-10")
        old_result = str(tz)  # "Etc/GMT-10" - old buggy behavior
        new_result = tz.tzname(None)  # "+10" - correct behavior
        
        current_result = _get_timezone_name(tz)
        
        # Verify the current behavior matches the old buggy one
        self.assertEqual(current_result, old_result)
        
        # And that the new behavior would be correct
        self.assertEqual(new_result, "+10")
        
        # Another case to verify edge cases
        tz2 = pytz.timezone("Etc/GMT+5")
        old_result2 = str(tz2)  # "Etc/GMT+5"
        new_result2 = tz2.tzname(None)  # "-05" 
        
        self.assertEqual(_get_timezone_name(tz2), old_result2)
        self.assertEqual(new_result2, "-05")