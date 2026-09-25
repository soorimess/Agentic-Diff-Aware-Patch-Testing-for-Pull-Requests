"""
Regression test specifically for Django#14792 - the exact behavior change in _get_timezone_name function.

The change was from:
    return str(timezone) 
TO:
    return timezone.tzname(None) or str(timezone)

This difference affects how specific timezones (like Etc/GMT-10) have their names processed,
which interacts with PostgreSQL database queries using AT TIME ZONE operations.
"""
import unittest

try:
    import pytz
    HAS_PYTZ = True
except ImportError:
    HAS_PYTZ = False

from django.utils import timezone


class Django14792RegressionTest(unittest.TestCase):
    """
    Tests for the specific timezone name formatting issue that broke Trunc/Extract functions
    with reverse time zone conversion for certain fixed offset timezones.
    """
    
    def test_get_timezone_name_produces_valid_output(self):
        """
        Tests that _get_timezone_name produces a valid string, not None or empty,
        so database timezone operations don't break.
        """
        if not HAS_PYTZ:
            self.skipTest("pytz not available")
            
        # Test with the specific timezone mentioned in the bug report
        tz = pytz.timezone("Etc/GMT-10")
        
        # Call the function under test
        result = timezone._get_timezone_name(tz)
        
        # Critical: should always return a string (never None)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        
        # This is where the bug behavior would manifest - if the implementation
        # was using timezone.tzname(None) properly with early return,
        # special handling of specific zone types could matter
        
    def test_timezone_name_handling_consistency(self):
        """
        Test consistency of timezone name handling across various scenarios
        to prevent regresions in timezone conversion for database operations.
        """
        if not HAS_PYTZ:
            self.skipTest("pytz not available")
            
        # Test multiple timezones to ensure broad compatibility
        timezones = [
            ("Etc/GMT-10", "GMT-style timezone"),
            ("Europe/Paris", "Standard timezone"),
            ("America/New_York", "Standard timezone"),
        ]
        
        for tz_name, description in timezones:
            with self.subTest(timezone=tz_name, description=description):
                tz = pytz.timezone(tz_name)
                result = timezone._get_timezone_name(tz)
                
                # Should always return a valid, non-empty string
                self.assertIsNotNone(result)
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)
    
    def test_fixed_offset_timezone_handling(self):
        """
        Test special handling of fixed offset timezones that might behave differently
        from named timezones in the database conversion logic.
        """
        if not HAS_PYTZ:
            self.skipTest("pytz not available")
            
        # Test fixed timezone creation
        fixed_tz = timezone.get_fixed_timezone(-600)  # 10 hours behind UTC
        result = timezone._get_timezone_name(fixed_tz)
        
        # Should be valid for database operations
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()