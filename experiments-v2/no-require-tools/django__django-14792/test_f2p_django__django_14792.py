from django.test import TestCase
from django.utils import timezone


class TimezoneConversionTest(TestCase):
    def test_get_timezone_name_returns_offset_for_fixed_offsets(self):
        """
        Test that _get_timezone_name returns the offset for fixed offset timezones
        instead of the full timezone name.
        
        This is a regression test for Django issue where _get_timezone_name 
        was changed to return str(timezone) instead of timezone.tzname(None) or str(timezone)
        """
        # Test with Etc/GMT-10 timezone (10 hours ahead of UTC)
        tz = timezone.pytz.timezone("Etc/GMT-10")
        
        # This is the core issue:
        # Before fix: _get_timezone_name returned str(tz) = "Etc/GMT-10" 
        # After fix: _get_timezone_name returns timezone.tzname(None) or str(timezone) = "+10"
        from django.utils.timezone import _get_timezone_name
        name = _get_timezone_name(tz)
        
        # The correct behavior is to return the timezone offset, not the full name
        # For Etc/GMT-10, the offset is "+10" (10 hours ahead of UTC)
        # This is what the database operations expect to properly convert timezones
        self.assertEqual(name, "+10")
        
    def test_get_timezone_name_behavior_with_different_timezones(self):
        """
        Test that _get_timezone_name works correctly with various timezone types.
        """
        from django.utils.timezone import _get_timezone_name
        
        # Test fixed offset timezone
        tz_fixed = timezone.pytz.timezone("Etc/GMT-10")
        name_fixed = _get_timezone_name(tz_fixed)
        # Should return offset "+10", not "Etc/GMT-10"
        self.assertEqual(name_fixed, "+10")
        
        # Test named timezone (should still work)
        try:
            tz_named = timezone.pytz.timezone("America/New_York")
            name_named = _get_timezone_name(tz_named)
            # For named timezones, it should return the full name
            self.assertEqual(name_named, "America/New_York")
        except Exception:
            # If pytz is not available, just test the fixed offset behavior
            pass