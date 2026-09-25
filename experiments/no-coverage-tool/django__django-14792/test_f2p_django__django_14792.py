"""
Regression test for Django issue #14792: Reverse time zone conversion
in Trunc()/Extract() database functions.

This test ensures that _get_timezone_name correctly returns timezone names 
rather than timespan offsets for fixed offset timezones.

The bug was that timezone._get_timezone_name(pytz.timezone("Etc/GMT-10")) 
returned "+10" instead of "Etc/GMT-10".

This test validates that the fix is present by asserting the new expected behavior.
"""

from django.test import TestCase
from django.utils import timezone as tz_utils
import pytz


class TimezoneNameFixTest(TestCase):
    def test_etc_gmt_timezone_name_is_full_name_not_offset(self):
        """
        The fix makes timezone names properly returned instead of offsets.
        This would have caused incorrect SQL generation in database operations.
        """
        # This specifically tests the reported bug case
        tz = pytz.timezone('Etc/GMT-10')
        tz_name = tz_utils._get_timezone_name(tz)
        
        # The bug was that this returned "+10" 
        # The fix makes this return "Etc/GMT-10"
        # This assertion should ENABLE with fix, FAIL without fix
        self.assertEqual(tz_name, 'Etc/GMT-10')

    def test_timezone_name_not_offset_for_simple_cases(self):
        """
        Test that various simple timezone cases return appropriate names.  
        """
        # Test UTC still works
        utc_tz = pytz.timezone('UTC')
        utc_name = tz_utils._get_timezone_name(utc_tz)
        self.assertEqual(utc_name, 'UTC')
        
        # Test regular timezone still works
        ny_tz = pytz.timezone('America/New_York')
        ny_name = tz_utils._get_timezone_name(ny_tz)
        self.assertEqual(ny_name, 'America/New_York')

    def test_etc_gmt_behavior_fix_specifically(self):
        """
        Specific test for the behavior change in response to Django issue #14792
        """
        tz = pytz.timezone('Etc/GMT-10')
        result = tz_utils._get_timezone_name(tz)
        
        # This test validates that the reported bug has been fixed
        # OLD BUGGY BEHAVIOR: result was "+10"  
        # NEW FIXED BEHAVIOR: result is "Etc/GMT-10"
        self.assertEqual(result, 'Etc/GMT-10')