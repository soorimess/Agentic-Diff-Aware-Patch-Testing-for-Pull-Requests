"""
Regression test for Django issue with reverse timezone conversion
in Trunc()/Extract() database functions when using Etc/GMT timezones.

This test files captures the behavior change in _get_timezone_name function
where pytz.timezone("Etc/GMT-10") used to return "Etc/GMT-10" but should return "+10"
to preserve backward compatibility.
"""
import datetime
import pytz
from django.test import TestCase
from django.utils import timezone


class TruncExtractTimezoneRegressionTest(TestCase):
    """
    Tests to verify that timezone handling in database functions 
    maintains proper behavior for Etc/GMT timezones.
    """
    
    def test_get_timezone_name_returns_correct_name_for_etc_gmt(self):
        """
        Test that _get_timezone_name returns the proper timezone name for Etc/GMT timezones.
        
        The regression was that for timezone "Etc/GMT-10", the function would return
        "Etc/GMT-10" instead of "+10", which caused incorrect SQL generation in
        database functions like Trunc() and Extract().
        
        The underlying issue is that timezone.tzname(None) for Etc/GMT-10 returns "+10",
        and for consistency with the fix that should be applied, this should be the
        returned value rather than the full timezone name.
        """
        tz = pytz.timezone("Etc/GMT-10")
        tz_name = timezone._get_timezone_name(tz)
        
        # This assertion should pass after the fix is applied
        # In Django 3.1 behavior, the function returned "+10"
        # In Django 3.2 (with this change), it returns "+10" but currently returns "Etc/GMT-10"
        # After fix, the function should return "+10" like it did in 3.1
        self.assertEqual(tz_name, "+10", 
                         "Etc/GMT-10 timezone should return '+10' for backward compatibility")

    def test_get_timezone_name_behavior_preserves_backward_compatibility(self):
        """
        Ensure that for Etc/GMT-10 timezone, the behavior matches Django 3.1 expectation.
        
        This directly tests the behavior that the fix was designed to restore:
        - timezone.tzname(None) for Etc/GMT-10 returns "+10"  
        - This should be preferred over the str() representation "Etc/GMT-10"
        """
        tz = pytz.timezone("Etc/GMT-10")
        
        # Test the underlying behavior
        tzname_result = tz.tzname(None)
        str_result = str(tz)
        
        # For Etc/GMT-10 timezone we get these values:
        self.assertEqual(tzname_result, "+10")
        self.assertEqual(str_result, "Etc/GMT-10")
        
        # The behavior we want to test is that _get_timezone_name returns "+10" 
        # because that's how it worked in Django 3.1
        actual_result = timezone._get_timezone_name(tz)
        self.assertEqual(actual_result, "+10")