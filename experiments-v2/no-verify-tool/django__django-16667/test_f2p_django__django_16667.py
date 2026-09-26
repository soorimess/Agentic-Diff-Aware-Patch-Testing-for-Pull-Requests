from django import forms
from django.forms import SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowErrorTest(TestCase):
    def test_select_date_widget_overflow_error(self):
        """
        Test that SelectDateWidget.value_from_datadict handles OverflowError
        when large integers are passed, returning "0-0-0" instead of crashing.
        """
        widget = SelectDateWidget()
        # This should not raise OverflowError but should return "0-0-0"
        data = {
            'my_date_year': '1234567821345678',
            'my_date_month': '1',
            'my_date_day': '1'
        }
        
        # This should not raise OverflowError
        result = widget.value_from_datadict(data, {}, 'my_date')
        
        # Before the fix, this would raise OverflowError
        # After the fix, this should return "0-0-0"
        self.assertEqual(result, "0-0-0")
        
    def test_select_date_widget_overflow_error_month(self):
        """
        Test that SelectDateWidget.value_from_datadict handles OverflowError
        when large month integer is passed.
        """
        widget = SelectDateWidget()
        # This should not raise OverflowError but should return "0-0-0"
        data = {
            'my_date_year': '2023',
            'my_date_month': '1234567821345678',
            'my_date_day': '1'
        }
        
        # This should not raise OverflowError
        result = widget.value_from_datadict(data, {}, 'my_date')
        
        # After the fix, this should return "0-0-0"
        self.assertEqual(result, "0-0-0")
        
    def test_select_date_widget_overflow_error_day(self):
        """
        Test that SelectDateWidget.value_from_datadict handles OverflowError
        when large day integer is passed.
        """
        widget = SelectDateWidget()
        # This should not raise OverflowError but should return "0-0-0"
        data = {
            'my_date_year': '2023',
            'my_date_month': '1',
            'my_date_day': '1234567821345678'
        }
        
        # This should not raise OverflowError
        result = widget.value_from_datadict(data, {}, 'my_date')
        
        # After the fix, this should return "0-0-0"
        self.assertEqual(result, "0-0-0")