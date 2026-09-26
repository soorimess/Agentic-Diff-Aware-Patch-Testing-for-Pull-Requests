"""
Test for Django issue #14792: Reverse time zone conversion in Trunc()/Extract() database functions.

This test verifies that timezone conversion works correctly for fixed offset timezones
like "Etc/GMT-10" where the behavior changed between Django 3.1 and 3.2.
"""
from django.test import TestCase
from django.utils import timezone
import pytz


class TruncExtractTimezoneTest(TestCase):
    def test_get_timezone_name_returns_offset_for_fixed_offset(self):
        """
        Test that _get_timezone_name returns offset for fixed offset timezones.
        
        The bug was that _get_timezone_name() returned "Etc/GMT-10" instead of "+10"
        for fixed offset timezones like Etc/GMT-10, causing incorrect SQL generation.
        """
        from django.utils.timezone import _get_timezone_name
        
        # Test with Etc/GMT-10 timezone - should return "+10" (the offset)
        tz = pytz.timezone("Etc/GMT-10")
        tzname = _get_timezone_name(tz)
        
        # This should return "+10" (the offset) not "Etc/GMT-10" (the full name)
        # This is what the fix should restore
        self.assertEqual(tzname, "+10")
        
    def test_get_timezone_name_positive_offset(self):
        """
        Test that _get_timezone_name returns correct offset for positive offset timezones.
        """
        from django.utils.timezone import _get_timezone_name
        
        # Test with Etc/GMT+5 timezone - should return "-05" (the offset)
        tz = pytz.timezone("Etc/GMT+5")
        tzname = _get_timezone_name(tz)
        
        # Should return "-05" for a timezone that is 5 hours ahead of UTC
        # (so when used in PostgreSQL AT TIME ZONE, it should be -5)
        self.assertEqual(tzname, "-05")
        
    def test_get_timezone_name_utc(self):
        """
        Test that _get_timezone_name works correctly with UTC.
        """
        from django.utils.timezone import _get_timezone_name
        
        # Test with UTC timezone
        tz = pytz.timezone("UTC")
        tzname = _get_timezone_name(tz)
        
        # Should return "UTC" for UTC (tzname(None) returns "UTC")
        self.assertEqual(tzname, "UTC")
        
    def test_timezone_name_behavior_matches_bug_report(self):
        """
        Test that demonstrates the exact issue described in the bug report.
        
        Before fix: timezone._get_timezone_name(pytz.timezone("Etc/GMT-10")) returned "Etc/GMT-10"
        After fix: timezone._get_timezone_name(pytz.timezone("Etc/GMT-10")) should return "+10"
        """
        from django.utils.timezone import _get_timezone_name
        
        # This is the exact test case from the bug report
        tz = pytz.timezone("Etc/GMT-10")
        result = _get_timezone_name(tz)
        
        # This should be "+10" not "Etc/GMT-10" 
        self.assertEqual(result, "+10")