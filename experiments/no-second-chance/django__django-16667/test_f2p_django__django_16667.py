"""
Regression test for Django issue where SelectDateWidget can crash with OverflowError.

This test ensures that when large integers are provided to SelectDateWidget.value_from_datadict,
it gracefully returns "0-0-0" instead of raising an OverflowError.
"""
from django import forms
from django.forms import SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowErrorTest(TestCase):
    def test_select_date_widget_overflow_error_handling(self):
        """
        Test that SelectDateWidget handles OverflowError gracefully by returning "0-0-0"
        instead of crashing when large integers are provided.
        """
        widget = SelectDateWidget()
        # This should not raise OverflowError but return "0-0-0"
        data = {
            'my_date_year': '1234567821345678',
            'my_date_month': '1', 
            'my_date_day': '1'
        }
        
        result = widget.value_from_datadict(data, {}, 'my_date')
        # Should return "0-0-0" instead of raising OverflowError
        self.assertEqual(result, "0-0-0")
    
    def test_select_date_widget_overflow_error_different_fields(self):
        """
        Test that SelectDateWidget handles OverflowError when any field (year, month, or day) 
        is too large.
        """
        widget = SelectDateWidget()
        # Test with overflow in month field
        data = {
            'my_date_year': '2023',
            'my_date_month': '1234567821345678', 
            'my_date_day': '1'
        }
        
        result = widget.value_from_datadict(data, {}, 'my_date')
        self.assertEqual(result, "0-0-0")
        
        # Test with overflow in day field
        data2 = {
            'my_date_year': '2023',
            'my_date_month': '1', 
            'my_date_day': '1234567821345678'
        }
        
        result2 = widget.value_from_datadict(data2, {}, 'my_date')
        self.assertEqual(result2, "0-0-0")