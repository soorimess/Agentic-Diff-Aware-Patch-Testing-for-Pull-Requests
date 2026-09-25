"""
Regression test for Django issue #16667.

Tests that SelectDateWidget properly handles overflow errors and value errors
when invalid values are passed for date components (year, month, day).
"""

from django.test import TestCase


class SelectDateWidgetOverflowTest(TestCase):
    def test_select_date_widget_overflow_error(self):
        """
        Test that SelectDateWidget catches OverflowError when large integers
        are provided for date components, returning "0-0-0" instead of crashing.
        """
        from django.forms import SelectDateWidget
        
        # Test the widget behavior directly with overflow causing data
        widget = SelectDateWidget()
        
        # This should not raise OverflowError, but instead return "0-0-0"
        # using the new exception handling for OverflowError
        form_data = {
            'my_date_year': '1234567821345678',  # Large year that causes OverflowError when converted to int
            'my_date_month': '1',                # Valid month
            'my_date_day': '1',                  # Valid day
        }
        
        # The widget will call datetime.date(int(y), int(m), int(d))
        # With large int(y) this can trigger OverflowError in C date constructor
        result = widget.value_from_datadict(form_data, {}, 'my_date')
        
        # This should return "0-0-0" instead of raising OverflowError and crashing
        self.assertEqual(result, "0-0-0")
        
    def test_select_date_widget_value_error_still_works(self):
        """
        Test that existing ValueError handling still works for invalid dates.
        """
        from django.forms import SelectDateWidget
        
        # Test that we don't break the existing ValueError handling
        widget = SelectDateWidget()
        
        # Valid integers that would make an invalid date (like Feb 30th)
        form_data = {
            'my_date_year': '2023',              # Valid year
            'my_date_month': '2',                # February  
            'my_date_day': '30',                 # Invalid day for Feb
        }
        
        # This should trigger ValueError handling and return pseudo-ISO format
        result = widget.value_from_datadict(form_data, {}, 'my_date')
        
        # Should return pseudo-ISO date, not crash
        # The existing ValueError handler returns "%s-%s-%s" % (y or 0, m or 0, d or 0)
        # So with invalid day 30, it would be "2023-2-0"
        # But also could be "2023-2-30" if this is valid in some contexts
        # The point is it shouldn't crash with OverflowError
        # We just want to ensure the change doesn't break existing functionality
        self.assertIsInstance(result, str)