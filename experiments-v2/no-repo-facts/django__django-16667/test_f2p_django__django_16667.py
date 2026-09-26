"""
Regression test for Django issue #16667: SelectDateWidget can crash with OverflowError.

This test verifies that SelectDateWidget properly handles large integer values
that would cause an OverflowError when passed to datetime.date().
"""
from django import forms
from django.forms import SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowErrorTest(TestCase):
    def test_select_date_widget_overflow_error_handling(self):
        """
        Test that SelectDateWidget handles OverflowError gracefully when
        large integers are passed as date components.
        
        Before the fix: OverflowError was raised
        After the fix: OverflowError should be caught and "0-0-0" returned
        """
        widget = SelectDateWidget()
        
        # Test with values that would cause OverflowError
        # Large number that causes OverflowError when passed to datetime.date()
        data = {
            'my_date_day': '1',
            'my_date_month': '1',
            'my_date_year': '1234567821345678',  # Large number that causes OverflowError
        }
        
        # This should not raise OverflowError but should return "0-0-0" 
        # (the fix adds OverflowError handling to return this)
        result = widget.value_from_datadict(data, {}, 'my_date')
        
        # Verify it doesn't crash with OverflowError and returns expected format
        self.assertIsInstance(result, str)
        # The fix specifically returns "0-0-0" for overflow cases
        self.assertEqual(result, "0-0-0")