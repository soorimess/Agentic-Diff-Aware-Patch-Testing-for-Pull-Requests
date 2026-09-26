from django import forms
from django.forms import SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowErrorTest(TestCase):
    def test_select_date_widget_overflow_error_handling(self):
        """Test that SelectDateWidget handles OverflowError gracefully."""
        widget = SelectDateWidget()
        
        # Test data that causes OverflowError
        data = {
            'my_date_day': '1',
            'my_date_month': '1',
            'my_date_year': '1234567821345678'  # Large number that causes OverflowError
        }
        
        # This should not raise OverflowError
        # Before fix: OverflowError would be raised
        # After fix: Should return "0-0-0" (as per the fix)
        try:
            result = widget.value_from_datadict(data, {}, 'my_date')
            # If we get here without exception, that's good
            # The fix should return "0-0-0" for overflow cases
            self.assertEqual(result, "0-0-0")
        except OverflowError:
            # If we get OverflowError, that means the fix is not applied
            self.fail("OverflowError was raised when it should be handled by the fix")

    def test_select_date_widget_normal_operation(self):
        """Test that SelectDateWidget still works normally for valid dates."""
        widget = SelectDateWidget()
        
        # Test with valid data
        data = {
            'my_date_day': '15',
            'my_date_month': '6', 
            'my_date_year': '2023'
        }
        
        result = widget.value_from_datadict(data, {}, 'my_date')
        # Should return a properly formatted date string
        self.assertIn('2023-06-15', result)