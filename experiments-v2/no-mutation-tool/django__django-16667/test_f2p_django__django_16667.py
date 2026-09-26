import datetime
import unittest
from django import forms
from django.forms import SelectDateWidget
from django.http import HttpResponse


class TestSelectDateWidgetOverflow(unittest.TestCase):
    def test_select_date_widget_overflow_error(self):
        """Test that SelectDateWidget handles OverflowError gracefully."""
        # Create a form with SelectDateWidget
        class ReproForm(forms.Form):
            my_date = forms.DateField(widget=SelectDateWidget())
        
        # Create data that would cause OverflowError when converted to date
        # The bug occurs with very large year values like 1234567821345678
        data = {
            'my_date_day': '1',
            'my_date_month': '1', 
            'my_date_year': '1234567821345678'  # This is large enough to cause OverflowError
        }
        
        form = ReproForm(data)
        
        # Before the fix, this would raise OverflowError
        # After the fix, this should not raise an exception
        try:
            is_valid = form.is_valid()
            # If we get here without exception, check the result
            if is_valid:
                # Valid form should have a date
                self.assertIsNotNone(form.cleaned_data.get('my_date'))
            else:
                # Invalid form should not crash
                self.assertTrue(True)  # Just ensure no crash
        except OverflowError:
            # This should not happen after the fix
            self.fail("OverflowError was raised when it should be handled gracefully")

    def test_select_date_widget_overflow_error_returns_zero_date(self):
        """Test that SelectDateWidget returns '0-0-0' on OverflowError."""
        # Create a form with SelectDateWidget
        class ReproForm(forms.Form):
            my_date = forms.DateField(widget=SelectDateWidget())
        
        # Create data that would cause OverflowError when converted to date
        data = {
            'my_date_day': '1',
            'my_date_month': '1', 
            'my_date_year': '1234567821345678'
        }
        
        form = ReproForm(data)
        
        # Get the raw value from the widget to test the specific behavior
        widget = form.fields['my_date'].widget
        value = widget.value_from_datadict(data, {}, 'my_date')
        
        # After the fix, this should return "0-0-0" instead of raising OverflowError
        self.assertEqual(value, "0-0-0")