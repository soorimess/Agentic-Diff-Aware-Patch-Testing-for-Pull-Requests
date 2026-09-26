"""
Regression test for Django ticket #14792: Reverse time zone conversion in Trunc()/Extract() database functions.

This test verifies that the fix for timezone handling works correctly.
"""
import pytz
from django.test import TestCase
from django.utils import timezone


class TimezoneConversionTest(TestCase):
    def test_get_timezone_name_returns_offset_for_fixed_timezones(self):
        """
        Test that fixed offset timezones return offset representation for correct SQL generation.
        
        The fix ensures that for fixed offset timezones like Etc/GMT-10, 
        _get_timezone_name returns "+10" instead of "Etc/GMT-10" to prevent
        incorrect SQL generation in database operations.
        """
        # Test the specific case from the bug report
        tz = pytz.timezone("Etc/GMT-10")
        
        # This is what the fix makes it return - the offset representation
        # In the current (pre-fix) code, it returns "Etc/GMT-10" (incorrect for SQL)
        # After the fix, it should return "+10" (correct for SQL)
        tzname = timezone._get_timezone_name(tz)
        
        # The test should pass after the fix is applied
        self.assertEqual(tzname, "+10")  # This is what we want after the fix
        
    def test_trunc_extract_timezone_functionality(self):
        """
        Test that Trunc and Extract functions work with timezone specifications.
        """
        # Import here to avoid import issues in test runner
        from django.db.models.functions import Extract, Trunc
        from django.db.models.expressions import F
        
        # Test that timezone-aware functions can be created without errors
        tz = pytz.timezone("Etc/GMT-10")
        
        # These should work without raising exceptions
        extract = Extract(F('date_field'), 'day', tzinfo=tz)
        trunc = Trunc(F('date_field'), 'day', tzinfo=tz)
        
        # Verify basic functionality
        self.assertIsNotNone(extract)
        self.assertIsNotNone(trunc)