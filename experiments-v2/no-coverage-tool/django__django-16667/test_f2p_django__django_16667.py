from django import forms
from django.forms import SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowErrorTest(TestCase):
    """Test that SelectDateWidget handles OverflowError gracefully."""

    def test_overflow_error_does_not_crash_form_validation(self):
        """
        Test that large integer values in SelectDateWidget don't cause OverflowError.
        
        This is a regression test for a bug where SelectDateWidget.value_from_datadict
        would raise OverflowError when user-provided large integers were passed to
        datetime.date() constructor, instead of handling the error gracefully.
        """
        # Create a form with SelectDateWidget
        class ReproForm(forms.Form):
            my_date = forms.DateField(widget=SelectDateWidget())
        
        # Test data that would cause OverflowError in the original code
        # Large numbers that exceed the maximum integer size for C long
        data = {
            'my_date_day': '1',
            'my_date_month': '1', 
            'my_date_year': '1234567821345678'  # Large number that causes OverflowError
        }
        
        # The form validation should not raise OverflowError
        # This test ensures the fix prevents the crash
        form = ReproForm(data)
        
        # This should not raise OverflowError - the fix prevents this crash
        # The form validation should complete without raising OverflowError
        try:
            is_valid = form.is_valid()
            # If we reach here, no OverflowError was raised - the fix is working
            # The test passes because the widget handled the overflow gracefully
        except OverflowError:
            # This is the bug - OverflowError should not be raised
            self.fail("OverflowError was raised when handling large integer values in SelectDateWidget")