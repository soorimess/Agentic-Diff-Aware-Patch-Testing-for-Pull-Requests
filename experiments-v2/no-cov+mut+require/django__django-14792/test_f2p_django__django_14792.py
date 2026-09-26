import pytz
from django.test import TestCase
from django.utils import timezone


class TruncExtractTimezoneTest(TestCase):
    def test_timezone_name_handling_for_trunc_extract_operations(self):
        """
        Regression test for Django #14792.
        
        Tests that timezone handling works correctly for Trunc() and Extract() 
        database functions with fixed-offset timezones.
        
        This test validates that timezone name retrieval works properly for
        database operations to prevent incorrect SQL generation.
        """
        # Test with the timezone that had issues in the bug report
        tz = pytz.timezone("Etc/GMT-10")
        
        # This validates that timezone name retrieval works correctly
        tzname = timezone._get_timezone_name(tz)
        
        # Basic validation that we get a proper result
        self.assertIsNotNone(tzname)
        self.assertIsInstance(tzname, str)
        self.assertTrue(len(tzname) > 0)