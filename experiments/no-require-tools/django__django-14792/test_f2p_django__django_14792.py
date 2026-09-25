"""
Regression test for Django #14792 - Reverse time zone conversion in Trunc()/Extract() database functions.

This test verifies that the _get_timezone_name function produces the correct behavior 
to avoid incorrect timezone conversion in PostgreSQL database functions like Trunc() and Extract().
"""
from django.utils import timezone
from django.test import TestCase


class TruncExtractTimezoneTest(TestCase):
    def test_get_timezone_name_returns_offset_for_etc_gmt(self):
        """
        Test that _get_timezone_name returns offset representations for Etc/GMT timezones.
        
        The bug was that in Django 3.2+, _get_timezone_name was changed to return 
        the full timezone name "Etc/GMT-10" instead of the offset "+10".
        This caused incorrect SQL generation via _prepare_tzname_delta().
        
        After applying the fix in timezone.py, the function correctly returns
        the offset representation that enables proper SQL generation.
        """
        # Test special Etc/GMT timezone name that has confusing convention
        tz = timezone.pytz.timezone("Etc/GMT-10")
        
        # The fix is supposed to make this return the offset name, not the full timezone name  
        timezone_name = timezone._get_timezone_name(tz)
        
        # Etc/GMT-10 means 10 hours ahead of UTC, so should return offset "+10"
        expected_correct = "+10"  
        
        # This will pass after the fix is applied and fail before (which is what we want)
        self.assertEqual(timezone_name, expected_correct,
                         f"Expected timezone name for Etc/GMT-10 to be '+10', got '{timezone_name}'")