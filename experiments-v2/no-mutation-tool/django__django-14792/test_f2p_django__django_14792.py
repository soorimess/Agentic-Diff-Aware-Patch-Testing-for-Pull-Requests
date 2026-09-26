import unittest
from django.utils import timezone
import pytz

class TimezoneNameTest(unittest.TestCase):
    def test_get_timezone_name_with_etc_gmt_minus_10(self):
        """
        Test that _get_timezone_name returns the correct timezone name for Etc/GMT-10.
        
        This test verifies the fix for the timezone conversion bug where
        _get_timezone_name(pytz.timezone("Etc/GMT-10")) was returning "Etc/GMT-10"
        instead of "+10" in Django 3.2, causing incorrect SQL generation.
        """
        tz = pytz.timezone("Etc/GMT-10")
        tzname = timezone._get_timezone_name(tz)
        
        # After the fix, this should return "+10" (the offset representation)
        # rather than "Etc/GMT-10" (the full timezone name)
        self.assertEqual(tzname, "+10")

    def test_get_timezone_name_with_etc_gmt_plus_10(self):
        """
        Test that _get_timezone_name returns the correct timezone name for Etc/GMT+10.
        """
        tz = pytz.timezone("Etc/GMT+10")
        tzname = timezone._get_timezone_name(tz)
        
        # Etc/GMT+10 represents -10 hours from UTC, so should return "-10"
        self.assertEqual(tzname, "-10")

    def test_get_timezone_name_with_regular_timezone(self):
        """
        Test that _get_timezone_name works normally with regular timezones.
        """
        tz = pytz.timezone("America/New_York")
        tzname = timezone._get_timezone_name(tz)
        
        # Regular timezones should return their name
        self.assertEqual(tzname, "America/New_York")