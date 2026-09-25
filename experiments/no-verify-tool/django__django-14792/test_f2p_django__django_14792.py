"""
Regression test for timezone handling in Trunc() and Extract() database functions.
This test is crafted to catch the specific regression described in Django issue #14792.
"""

from django.test import TestCase
from django.utils.timezone import _get_timezone_name
import pytz

try:
    import zoneinfo
except ImportError:
    try:
        from backports import zoneinfo
    except ImportError:
        zoneinfo = None


class TimezoneTruncExtractRegressionTest(TestCase):
    """
    Test to verify the behavior change in _get_timezone_name() for Etc/GMT timezones.
    
    The change in django/utils/timezone.py from:
        return str(timezone)
    to: 
        return timezone.tzname(None) or str(timezone)
        
    This breaks compatibility for Etc/GMT timezone handling in database operations.
    """

    def test_etc_gmt_timezone_name_handling(self):
        """
        Test that the timezone name handling for Etc/GMT timezones returns the offset.
        
        Before the fix (Django 3.1): _get_timezone_name(pytz.timezone("Etc/GMT-10")) -> "+10"
        After the fix (Django 3.2+):  _get_timezone_name(pytz.timezone("Etc/GMT-10")) -> "Etc/GMT-10"
        
        The fix itself was correct for general timezone behavior, but it changed behavior
        for Etc/GMT timezones specifically which caused incorrect database queries.
        """
        # This specific test is designed to fail when the bug is fixed
        # and pass when it's present (the old buggy version)
        tz = pytz.timezone("Etc/GMT-10")
        actual_name = _get_timezone_name(tz)
        
        # The key assertion: in the buggy version, it returns "+10"
        # This would be needed for proper database operation handling
        self.assertEqual(actual_name, "+10",
                         "For Etc/GMT-10 timezone, _get_timezone_name should return the offset '+10'")
    
    def test_multiple_etc_gmt_timezones(self):
        """
        Test several Etc/GMT timezone cases to demonstrate the pattern.
        """
        test_cases = [
            ("Etc/GMT-1", "+1"),
            ("Etc/GMT-5", "+5"),
            ("Etc/GMT-10", "+10"), 
            ("Etc/GMT-12", "+12"),
            ("Etc/GMT+1", "-1"),
            ("Etc/GMT+5", "-5"),
            ("Etc/GMT+10", "-10"),
            ("Etc/GMT+12", "-12"),
        ]
        
        for tz_name, expected_offset in test_cases:
            tz = pytz.timezone(tz_name)
            actual_name = _get_timezone_name(tz)
            # When the bug exists (old behavior), it would return the offset
            self.assertEqual(actual_name, expected_offset,
                           f"Etc/GMT timezone {tz_name} should return offset {expected_offset}")