"""
Regression test for Django issue #16667.
Tests that SelectDateWidget handles OverflowError gracefully.
"""
import datetime
import sys
from django import forms
from django.forms import SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowErrorTest(TestCase):
    def test_select_date_widget_overflow_error_direct(self):
        """
        Test that SelectDateWidget.value_from_datadict handles OverflowError 
        when large integers are passed as date components.
        """
        widget = SelectDateWidget()
        
        # Test with large year that causes OverflowError
        data = {
            'my_date_day': '1',
            'my_date_month': '1',
            'my_date_year': str(sys.maxsize + 1)  # This will cause OverflowError
        }
        
        # This should return "0-0-0" instead of raising OverflowError after the fix
        # Before the fix, this raises OverflowError
        try:
            result = widget.value_from_datadict(data, {}, 'my_date')
            # If we get here without exception, check the result
            self.assertEqual(result, "0-0-0")
        except OverflowError:
            # This is the bug - it should not raise OverflowError
            self.fail("SelectDateWidget.value_from_datadict raised OverflowError when processing large year value")
            
    def test_select_date_widget_normal_values_still_work(self):
        """
        Ensure normal date values still work correctly.
        """
        widget = SelectDateWidget()
        
        # Test with normal values
        data = {
            'my_date_day': '15',
            'my_date_month': '6', 
            'my_date_year': '2023'
        }
        
        result = widget.value_from_datadict(data, {}, 'my_date')
        # Should return a properly formatted date string
        self.assertEqual(result, "2023-06-15")
        
    def test_select_date_widget_invalid_values_still_return_pseudo_iso(self):
        """
        Ensure invalid date values still return pseudo-ISO format.
        """
        widget = SelectDateWidget()
        
        # Test with invalid date values (should trigger ValueError handler)
        data = {
            'my_date_day': '31',
            'my_date_month': '2',  # February never has 31 days
            'my_date_year': '2023'
        }
        
        result = widget.value_from_datadict(data, {}, 'my_date')
        # Should return pseudo-ISO format with zeros for invalid values
        self.assertEqual(result, "2023-2-31")