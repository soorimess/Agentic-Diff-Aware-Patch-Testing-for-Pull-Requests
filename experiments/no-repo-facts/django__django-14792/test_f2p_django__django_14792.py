import pytz
from django.test import TestCase
from django.utils import timezone


class Django14792TimezoneRegressionTest(TestCase):
    """
    Regression test for Django Issue #14792:
    Reverse time zone conversion in Trunc()/Extract() database functions.
    
    The bug: timezone._get_timezone_name() returns "Etc/GMT-10" instead of "+10"
    for Etc/GMT timezone objects, causing incorrect PostgreSQL SQL generation.
    """

    def test_get_timezone_name_returns_correct_format_for_etc_gmt(self):
        """
        This test demonstrates the exact behavior that changed in Django 3.2.
        Before fix: _get_timezone_name(pytz.timezone("Etc/GMT-10")) returned "Etc/GMT-10"
        After fix: _get_timezone_name(pytz.timezone("Etc/GMT-10")) should return "+10"
        
        When the test fails, it means the buggy behavior is still present.
        When the test passes, it means the fix is working.
        """
        # Target timezone from the bug report
        tz = pytz.timezone("Etc/GMT-10")
        
        # Check what we currently get
        timezone_name = timezone._get_timezone_name(tz)
        
        # This assertion currently FAILS (meaning the bug exists)
        # After the fix is applied, it should PASS 
        self.assertEqual(
            timezone_name, 
            "+10",  # The fix makes it return the offset
            "Bug present: timezone._get_timezone_name should return offset '+10' for Etc/GMT-10"
        )