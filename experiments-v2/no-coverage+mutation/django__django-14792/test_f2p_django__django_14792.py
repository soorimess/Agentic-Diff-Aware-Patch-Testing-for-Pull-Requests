import unittest

import pytz
from django.test import TestCase
from django.utils import timezone

try:
    import zoneinfo
except ImportError:
    zoneinfo = None


class TimezoneNameTest(TestCase):
    def test_get_timezone_name_for_etc_gmt_zones(self):
        """
        Test that _get_timezone_name returns the correct value for Etc/GMT timezones.
        
        This is a regression test for Django issue #14792.
        For Etc/GMT-10 timezone, the behavior changed between Django 3.1 and 3.2.
        """
        # Test with pytz
        etc_gmt_minus_10 = pytz.timezone("Etc/GMT-10")
        result = timezone._get_timezone_name(etc_gmt_minus_10)
        
        # In Django 3.1, this would return "+10" (the offset)
        # In Django 3.2+, this returns "Etc/GMT-10" (the timezone name) - this is the bug
        # The correct behavior should be to return the offset for fixed offset timezones
        self.assertEqual(result, "+10")

    def test_get_timezone_name_for_etc_gmt_plus_5(self):
        """
        Test that _get_timezone_name returns the correct value for Etc/GMT+5 timezone.
        """
        etc_gmt_plus_5 = pytz.timezone("Etc/GMT+5")
        result = timezone._get_timezone_name(etc_gmt_plus_5)
        
        # For Etc/GMT+5, the offset should be "-05" 
        self.assertEqual(result, "-05")

    def test_get_timezone_name_for_etc_gmt_zones_with_zoneinfo(self):
        """
        Test that _get_timezone_name returns the correct value for Etc/GMT timezones with zoneinfo.
        """
        if zoneinfo is None:
            self.skipTest("zoneinfo not available")
            
        etc_gmt_minus_10 = zoneinfo.ZoneInfo("Etc/GMT-10")
        result = timezone._get_timezone_name(etc_gmt_minus_10)
        
        # Same issue applies to zoneinfo
        self.assertEqual(result, "+10")