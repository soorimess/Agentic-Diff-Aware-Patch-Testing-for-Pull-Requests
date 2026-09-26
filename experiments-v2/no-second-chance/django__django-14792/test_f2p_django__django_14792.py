"""
Regression test for Django ticket #14792 - Reverse time zone conversion in Trunc()/Extract() database functions.

This test verifies the behavior of _get_timezone_name() for Etc/GMT timezones
to ensure database query generation works correctly.
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


class TruncExtractTimezoneTest(unittest.TestCase):
    
    def test_get_timezone_name_etc_gmt_returns_offset_not_name(self):
        """
        Test that _get_timezone_name() returns offset representation for Etc/GMT timezones.
        
        The bug was that _get_timezone_name() was changed to return timezone names
        instead of offset representations, which broke database query generation.
        
        For Etc/GMT-10, we want "+10" (offset) not "Etc/GMT-10" (timezone name)
        because database operations expect the offset format.
        """
        # Test Etc/GMT timezone
        etc_gmt_10 = pytz.timezone("Etc/GMT-10")
        
        # The behavior that should be preserved for database compatibility
        # is to return the offset representation, not the timezone name
        result = timezone._get_timezone_name(etc_gmt_10)
        
        # For Etc/GMT-10, the offset is +10 hours (10 hours ahead of UTC)
        # The database operations expect this offset representation
        self.assertEqual(result, "+10", 
                        "Expected offset representation for database compatibility")
        
    def test_get_timezone_name_consistency(self):
        """
        Test consistency of _get_timezone_name behavior across different timezone types.
        """
        # Test with standard timezone
        paris = pytz.timezone("Europe/Paris")
        result = timezone._get_timezone_name(paris)
        self.assertIsInstance(result, str)
        
        # Test with Etc/GMT timezone
        etc_gmt_10 = pytz.timezone("Etc/GMT-10")
        result = timezone._get_timezone_name(etc_gmt_10)
        self.assertIsInstance(result, str)
        
    @unittest.skipIf(not zoneinfo, "zoneinfo not available")
    def test_get_timezone_name_zoneinfo_consistency(self):
        """
        Test _get_timezone_name behavior with zoneinfo (Python 3.9+).
        """
        # Test with zoneinfo if available
        etc_gmt_10 = zoneinfo.ZoneInfo("Etc/GMT-10")
        result = timezone._get_timezone_name(etc_gmt_10)
        self.assertIsInstance(result, str)