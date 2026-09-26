import sys
from django.forms import SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowErrorTest(TestCase):
    """Test that SelectDateWidget handles OverflowError gracefully."""

    def test_overflow_error_in_value_from_datadict(self):
        """
        Test that SelectDateWidget catches OverflowError in value_from_datadict.
        
        Before the fix: OverflowError was raised
        After the fix: '0-0-0' should be returned
        """
        widget = SelectDateWidget()
        
        # Test data that would cause OverflowError in datetime.date()
        data = {
            'my_date_day': '1',
            'my_date_month': '1',
            'my_date_year': str(sys.maxsize + 1)  # This causes OverflowError
        }
        
        # This should not raise OverflowError
        # It should return '0-0-0' after the fix
        try:
            result = widget.value_from_datadict(data, {}, 'my_date')
            # If we get here without exception, the fix is working
            # The expected result after fix is '0-0-0'
            self.assertEqual(result, "0-0-0")
        except OverflowError:
            self.fail("OverflowError was raised when it should be handled gracefully")