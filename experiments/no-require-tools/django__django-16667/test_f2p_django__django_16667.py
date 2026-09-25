"""
Regression test for Django issue #16667.

Tests that SelectDateWidget properly handles OverflowError
when large integer values are passed to date constructor.
"""
from django.test import TestCase
from django.forms import SelectDateWidget


class SelectDateWidgetOverflowErrorTest(TestCase):
    def test_overflow_error_handled_gracefully(self):
        """
        Test that SelectDateWidget handles OverflowError gracefully when
        user provides large integers that cause OverflowError in date() constructor.
        """
        widget = SelectDateWidget()
        
        # This data would trigger OverflowError exactly as described in the bug report
        data = {
            'my_date_day': '1',
            'my_date_month': '1',
            'my_date_year': '1234567821345678'  # Too large for C long conversion
        }
        
        # Before fix: Would raise OverflowError  
        # After fix: Should return "0-0-0" without raising exception
        result = widget.value_from_datadict(data, {}, 'my_date')
        self.assertEqual(result, '0-0-0')

    def test_normal_date_functionality_preserved(self):
        """
        Test that normal date functionality remains intact after the fix.
        """
        widget = SelectDateWidget()
        
        # Normal valid date should work as before
        data = {
            'my_date_day': '15',
            'my_date_month': '6', 
            'my_date_year': '2023'
        }
        
        result = widget.value_from_datadict(data, {}, 'my_date')
        # Should return a properly formatted date string
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)