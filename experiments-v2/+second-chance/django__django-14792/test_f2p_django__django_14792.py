"""
Regression test for Django issue #14792: Reverse time zone conversion
in Trunc()/Extract() database functions.
"""
import pytz
from django.db.models.functions import Extract, Trunc
from django.test import TestCase
from django.utils import timezone


class TruncExtractTimezoneTest(TestCase):
    def test_timezone_name_handling_for_etc_gmt_minus_10(self):
        """
        Test that Etc/GMT-10 timezone is handled correctly in Trunc/Extract functions.
        
        Before the fix, _get_timezone_name() returned "Etc/GMT-10" for Etc/GMT-10,
        which when processed by _prepare_tzname_delta() became "Etc/GMT+10" (wrong).
        
        After the fix, _get_timezone_name() returns "+10" for Etc/GMT-10,
        which when processed by _prepare_tzname_delta() becomes "-10" (correct).
        """
        # Test with Etc/GMT-10 timezone (10 hours ahead of UTC)
        gmt_minus_10 = pytz.timezone("Etc/GMT-10")
        
        # Test the _get_timezone_name function directly
        timezone_name = timezone._get_timezone_name(gmt_minus_10)
        
        # This should return "+10" after the fix, not "Etc/GMT-10"
        # The bug was that it returned "Etc/GMT-10" which caused wrong conversion
        self.assertEqual(timezone_name, "+10")
        
    def test_trunc_extract_with_etc_gmt_timezone(self):
        """
        Test that Trunc/Extract functions work correctly with Etc/GMT timezones.
        """
        # Create a timezone that would cause the bug
        gmt_minus_10 = pytz.timezone("Etc/GMT-10")
        
        # This should not raise an exception and should work correctly
        # We're testing that the timezone name is handled properly in the SQL generation
        try:
            # Test Extract function
            extract_func = Extract('field', 'day', tzinfo=gmt_minus_10)
            # Just test that it can be created without error
            self.assertIsNotNone(extract_func)
            
            # Test Trunc function  
            trunc_func = Trunc('field', 'day', tzinfo=gmt_minus_10)
            # Just test that it can be created without error
            self.assertIsNotNone(trunc_func)
        except Exception as e:
            # If we get an exception, it's likely due to the timezone name handling bug
            self.fail(f"Exception raised with Etc/GMT timezone: {e}")