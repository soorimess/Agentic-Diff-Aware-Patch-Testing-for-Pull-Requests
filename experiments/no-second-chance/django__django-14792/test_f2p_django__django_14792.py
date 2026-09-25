"""
Regression test for Django #14792 - Reverse timezone conversion in Trunc()/Extract() 
database functions with Etc/GMT timezones.
"""
from django.test import TestCase
from django.utils.timezone import _get_timezone_name
import pytz


class TimezoneConversionTest(TestCase):
    def test_get_timezone_name_for_etc_gmt_fixed_offset(self):
        """
        Test that _get_timezone_name returns offset for Etc/GMT fixed offset timezones.
        
        The issue was that _get_timezone_name would return the full timezone name
        instead of the offset representation for fixed offset timezones like Etc/GMT-10.
        This would cause incorrect SQL generation in database operations.
        """
        # Test with Etc/GMT-10 timezone (10 hours east of UTC)
        tz = pytz.timezone("Etc/GMT-10")
        result = _get_timezone_name(tz)
        
        # The bug was that _get_timezone_name("Etc/GMT-10") would return "Etc/GMT-10"
        # but should return "+10" to correctly represent the 10-hour positive offset
        # In Django 3.1 this returned "+10", in 3.2 it incorrectly returned "Etc/GMT-10"
        # The fix should make it return "+10" again
        self.assertEqual(result, "+10")

    def test_get_timezone_name_for_etc_gmt_negative_offset(self):
        """
        Test that _get_timezone_name correctly handles negative offset Etc/GMT timezones.
        """
        # Test with Etc/GMT+5 timezone (5 hours west of UTC) 
        tz = pytz.timezone("Etc/GMT+5")
        result = _get_timezone_name(tz)
        
        # For Etc/GMT+5, tzname(None) should return "-0500"
        # This represents 5 hours west, which is correct for the database query interpretation
        expected = "-0500"
        self.assertEqual(result, expected)

    def test_get_timezone_name_for_regular_timezone_unchanged(self):
        """
        Test that _get_timezone_name still works correctly for regular timezone names.
        This behavior should not be affected by the fix.
        """
        # Test with a regular timezone that should return full name
        tz = pytz.timezone("America/New_York")
        result = _get_timezone_name(tz)
        
        # For regular timezones, should return the timezone name
        self.assertEqual(result, "America/New_York")
        
    def test_get_timezone_name_with_zoneinfo(self):
        """
        Test that _get_timezone_name works with zoneinfo (Python 3.9+).
        """
        try:
            import zoneinfo
            tz = zoneinfo.ZoneInfo("Etc/GMT-8")
            result = _get_timezone_name(tz)
            # Should return offset form for fixed offset timezones
            self.assertEqual(result, "+08")
        except ImportError:
            # zoneinfo is not available in older Python versions
            pass