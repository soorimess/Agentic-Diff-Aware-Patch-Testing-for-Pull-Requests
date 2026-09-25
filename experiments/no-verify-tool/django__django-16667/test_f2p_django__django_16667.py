"""
Regression test for Django issue where SelectDateWidget can crash with OverflowError.

This test verifies that when large integers are provided to SelectDateWidget,
instead of raising an OverflowError, it returns "0-0-0" as a fallback.
"""
from django import forms
from django.forms import SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowTest(TestCase):
    def test_select_date_widget_handles_overflow_error_gracefully(self):
        """
        Test that SelectDateWidget catches OverflowError and returns "0-0-0".
        
        This test specifically targets the behavior change in the fix:
        - Before fix: OverflowError was raised from datetime.date() call 
        - After fix: OverflowError is caught and "0-0-0" is returned
        
        The test demonstrates that large integers (too large for C long) now
        are handled gracefully rather than crashing the server.
        """
        # Create form with SelectDateWidget as in the bug report
        class ReproForm(forms.Form):
            my_date = forms.DateField(widget=SelectDateWidget())
        
        # This exact data from the bug report causes OverflowError 
        data = {
            'my_date_day': '1',
            'my_date_month': '1', 
            'my_date_year': '1234567821345678'  # Causes OverflowError
        }
        
        form = ReproForm(data)
        widget = form.fields['my_date'].widget
        
        # This should return "0-0-0" instead of raising OverflowError
        result = widget.value_from_datadict(data, {}, 'my_date')
        
        # The fix makes it return "0-0-0" for overflows instead of crashing
        self.assertEqual(result, "0-0-0")