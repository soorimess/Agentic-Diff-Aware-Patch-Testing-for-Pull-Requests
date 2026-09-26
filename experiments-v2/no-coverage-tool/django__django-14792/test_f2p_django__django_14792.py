"""
Regression test for Django issue #14792: Reverse time zone conversion in Trunc()/Extract() database functions.

This test verifies that timezone names for fixed offset timezones are handled correctly
in the _get_timezone_name() function, ensuring that PostgreSQL operations receive
the correct offset format for timezone conversion.
"""
import pytz
from django.test import TestCase
from django.utils import timezone


class TruncExtractTimezoneTest(TestCase):
    def test_get_timezone_name_returns_offset_for_fixed_offsets(self):
        """
        Test that _get_timezone_name() returns offset for fixed offset timezones.
        
        For timezones like "Etc/GMT-10", the function should return "+10" (the offset)
        rather than "Etc/GMT-10" (the timezone name) to ensure correct PostgreSQL
        timezone conversion.
        """
        # Test the specific case mentioned in the bug report
        tz = pytz.timezone("Etc/GMT-10")
        
        # This should return the offset "+10" to ensure correct conversion in PostgreSQL
        # The old (correct) behavior returned "+10"
        # The new (incorrect) behavior returns "Etc/GMT-10" 
        timezone_name = timezone._get_timezone_name(tz)
        
        # The fix ensures that fixed offset timezones return their offset,
        # not their full timezone name, so PostgreSQL operations can correctly
        # convert the sign
        self.assertEqual(timezone_name, "+10")
        
    def test_get_timezone_name_for_other_fixed_offsets(self):
        """
        Test that other fixed offset timezones also return correct offsets.
        """
        # Test Etc/GMT+5 (5 hours behind UTC) 
        tz = pytz.timezone("Etc/GMT+5")
        timezone_name = timezone._get_timezone_name(tz)
        # Should return offset "-05", not "Etc/GMT+5"
        self.assertEqual(timezone_name, "-05")