"""
Regression test for Django issue #16667.

This test ensures that SelectDateWidget handles OverflowError when large
integer values are passed to the date constructor.
"""
from django.forms import DateField, Form, SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowErrorTest(TestCase):
    def test_select_date_widget_overflow_error_direct(self):
        """
        Test that SelectDateWidget.value_from_datadict handles OverflowError gracefully.
        """
        widget = SelectDateWidget()
        data = {
            'my_date_day': '1',
            'my_date_month': '1', 
            'my_date_year': '1234567821345678',  # Large number that causes OverflowError
        }
        
        # This should not raise OverflowError but should return "0-0-0"
        # as per the fix in the pull request
        result = widget.value_from_datadict(data, {}, 'my_date')
        # If we get here without exception, the fix is working
        self.assertEqual(result, "0-0-0")
        
    def test_select_date_widget_overflow_error_form_validation(self):
        """
        Test that forms with SelectDateWidget don't crash with OverflowError.
        """
        class TestForm(Form):
            my_date = DateField(widget=SelectDateWidget())
        
        data = {
            'my_date_day': '1',
            'my_date_month': '1', 
            'my_date_year': '1234567821345678',  # Large number that causes OverflowError
        }
        
        # The form should not crash with OverflowError during validation
        form = TestForm(data)
        # This should not raise OverflowError
        # It may have validation errors for other reasons, but not OverflowError
        try:
            is_valid = form.is_valid()
            # If we get here without OverflowError, that's good
            # The form validation may fail for other reasons (invalid date format "0-0-0")
            # but it should not fail with OverflowError
        except OverflowError:
            self.fail("OverflowError was raised during form validation")