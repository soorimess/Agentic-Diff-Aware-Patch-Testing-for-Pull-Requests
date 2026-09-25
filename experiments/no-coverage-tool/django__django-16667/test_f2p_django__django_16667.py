"""
Regression test for Django issue #16667: SelectDateWidget can crash with OverflowError.
"""
from django import forms
from django.forms import SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowErrorTest(TestCase):
    def test_select_date_widget_overflow_error_returns_zero_date(self):
        """
        Test that SelectDateWidget handles OverflowError gracefully by returning 
        "0-0-0" instead of raising OverflowError.
        This is the main behavior change from the fix.
        """
        widget = SelectDateWidget()
        data = {
            'my_date_day': '1',
            'my_date_month': '1',
            'my_date_year': '1234567821345678'  # Large integer that causes OverflowError
        }
        
        # This should not raise OverflowError but return "0-0-0"
        result = widget.value_from_datadict(data, {}, 'my_date')
        
        # With the fix, should return "0-0-0" instead of raising OverflowError
        self.assertEqual(result, "0-0-0")


    def test_select_date_widget_overflow_error_no_crash_in_form(self):
        """
        Test that SelectDateWidget in a form doesn't crash with OverflowError
        when submitted with large integer values.
        """
        class ReproForm(forms.Form):
            my_date = forms.DateField(widget=SelectDateWidget())
            
        # Test case that previously caused OverflowError during form validation
        data = {
            'my_date_day': '1',
            'my_date_month': '1', 
            'my_date_year': '1234567821345678'  # Large integer that causes OverflowError
        }
        
        form = ReproForm(data)
        
        # Before the fix, this would raise OverflowError during form validation
        # After the fix, this should not crash - it might be invalid but not crash
        try:
            # Don't access cleaned_data which might trigger more issues, just 
            # validate using is_valid which should not raise OverflowError
            form.is_valid()
            # If we reach here without OverflowError, the fix works
            self.assertTrue(True)  # Test passed - no crash
        except OverflowError:
            self.fail("SelectDateWidget in form raised OverflowError with large integer year")