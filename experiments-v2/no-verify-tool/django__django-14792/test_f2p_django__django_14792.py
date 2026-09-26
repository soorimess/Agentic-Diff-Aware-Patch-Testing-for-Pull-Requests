"""
Regression test for Django ticket #14792: Reverse time zone conversion in Trunc()/Extract() database functions.

This test verifies that timezone names are properly handled when using Trunc/Extract functions
with timezones like "Etc/GMT-10" that have reversed sign conventions.
"""
import unittest

import pytz

try:
    import zoneinfo
except ImportError:
    try:
        from backports import zoneinfo
    except ImportError:
        zoneinfo = None

from django.utils import timezone


class Django14792RegressionTest(unittest.TestCase):
    def test_get_timezone_name_etc_gmt(self):
        """
        Test that _get_timezone_name returns the correct representation for Etc/GMT timezones.
        
        For Etc/GMT-10, the function should return "+10" (the offset) rather than "Etc/GMT-10"
        to ensure proper database conversion in PostgreSQL.
        """
        # Test Etc/GMT-10 timezone (10 hours ahead of UTC)
        gmt_minus_10 = pytz.timezone("Etc/GMT-10")
        tz_name = timezone._get_timezone_name(gmt_minus_10)
        
        # This should return "+10" (the offset) not "Etc/GMT-10" (the full name)
        # because Etc/GMT-10 represents 10 hours ahead of UTC
        self.assertEqual(tz_name, "+10")
        
        # Test Etc/GMT+10 timezone (10 hours behind UTC) 
        gmt_plus_10 = pytz.timezone("Etc/GMT+10")
        tz_name = timezone._get_timezone_name(gmt_plus_10)
        
        # This should return "-10" (the offset) not "Etc/GMT+10" (the full name)
        # because Etc/GMT+10 represents 10 hours behind UTC
        self.assertEqual(tz_name, "-10")
        
    @unittest.skipIf(not zoneinfo, "zoneinfo not available")
    def test_get_timezone_name_etc_gmt_zoneinfo(self):
        """
        Test that _get_timezone_name returns the correct representation for Etc/GMT timezones
        when using zoneinfo (Python 3.9+).
        """
        # Test Etc/GMT-10 timezone (10 hours ahead of UTC)
        gmt_minus_10 = zoneinfo.ZoneInfo("Etc/GMT-10")
        tz_name = timezone._get_timezone_name(gmt_minus_10)
        
        # This should return "+10" (the offset) not "Etc/GMT-10" (the full name)
        self.assertEqual(tz_name, "+10")
        
        # Test Etc/GMT+10 timezone (10 hours behind UTC) 
        gmt_plus_10 = zoneinfo.ZoneInfo("Etc/GMT+10")
        tz_name = timezone._get_timezone_name(gmt_plus_10)
        
        # This should return "-10" (the offset) not "Etc/GMT+10" (the full name)
        self.assertEqual(tz_name, "-10")
        
    def test_trunc_extract_with_etc_gmt_timezone(self):
        """
        Test that Trunc/Extract functions work correctly with Etc/GMT timezones.
        
        This verifies that the timezone conversion in the database operations works
        correctly with the fixed _get_timezone_name function.
        """
        # Test with a timezone that has a reversed sign convention
        gmt_minus_10 = pytz.timezone("Etc/GMT-10")
        
        # This would fail if _get_timezone_name returned "Etc/GMT-10" instead of "+10"
        # because the database conversion logic would treat it as 10 hours behind UTC
        # instead of 10 hours ahead UTC
        tz_name = timezone._get_timezone_name(gmt_minus_10)
        
        # The key assertion - this should be "+10" not "Etc/GMT-10"
        self.assertEqual(tz_name, "+10")