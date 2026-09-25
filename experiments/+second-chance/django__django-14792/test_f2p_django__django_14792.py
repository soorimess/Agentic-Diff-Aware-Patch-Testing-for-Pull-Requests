"""
Regression test for Django Etc/GMT timezone _get_timezone_name() issue.

This test ensures backward compatibility in timezone handling for database functions.
"""

from django.utils import timezone
from django.test import TestCase
import pytz


class TimezoneNameRegressionTest(TestCase):
    def test_etc_gmt_timezone_returns_offset_name(self):
        """
        Test that Etc/GMT timezone returns offset name for database compatibility.
        
        Before the fix: _get_timezone_name(pytz.timezone("Etc/GMT-10")) returned "Etc/GMT-10"
        After the fix: _get_timezone_name(pytz.timezone("Etc/GMT-10")) should return "+10" 
        """
        tz = pytz.timezone("Etc/GMT-10")
        tz_name = timezone._get_timezone_name(tz)
        
        # This should be the offset notation so database functions work correctly
        self.assertEqual(tz_name, "+10")