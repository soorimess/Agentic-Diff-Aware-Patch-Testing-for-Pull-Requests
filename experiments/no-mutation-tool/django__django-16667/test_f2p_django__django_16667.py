"""
Regression test for Django issue: SelectDateWidget can crash with OverflowError.

This test ensures that when large integers are passed to 
SelectDateWidget.value_from_datadict that would cause an OverflowError
in datetime.date(), the widget gracefully returns "0-0-0" instead
of raising an exception.
"""
from django.forms import DateField, Form, SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowErrorTest(TestCase):
    def test_select_date_widget_overflow_error(self):
        """
        Test that SelectDateWidget handles OverflowError gracefully by returning "0-0-0".
        
        When large integers are passed that would cause OverflowError in 
        datetime.date(int(y), int(m), int(d)), the widget should return "0-0-0"
        instead of raising an exception.
        """
        # Create a form with a SelectDateWidget
        class TestForm(Form):
            my_date = DateField(widget=SelectDateWidget())
        
        # Test case that would cause OverflowError
        # This specifically tests the bug where large year values cause OverflowError
        data = {
            'my_date_day': '1',
            'my_date_month': '1', 
            'my_date_year': '1234567821345678'  # Large year value that causes OverflowError
        }
        
        form = TestForm(data)
        
        # The form validation should not raise OverflowError
        # Instead, it should gracefully handle it and return "0-0-0"
        # We test this by accessing the cleaned_data and ensuring no exception is raised
        try:
            is_valid = form.is_valid()
            # If we reach here without exception, that's good
            # Now check the actual value returned by the widget
            if is_valid:
                # If form is valid, we access the cleaned data
                cleaned_date = form.cleaned_data.get('my_date')
            else:
                # If form is not valid, we check the raw data
                # The widget's value_from_datadict should return "0-0-0" 
                # instead of raising OverflowError
                widget_value = form.fields['my_date'].widget.value_from_datadict(
                    data, {}, 'my_date'
                )
                self.assertEqual(widget_value, "0-0-0")
        except OverflowError:
            # If this fails, it means the OverflowError was not caught
            self.fail("OverflowError was not handled by SelectDateWidget")

    def test_select_date_widget_overflow_error_with_zero_values(self):
        """
        Test that the widget still works normally with zero values.
        This ensures we don't break existing behavior.
        """
        class TestForm(Form):
            my_date = DateField(widget=SelectDateWidget())
        
        # Test with zero date values (should return zero formatted date)
        data = {
            'my_date_day': '0',
            'my_date_month': '0', 
            'my_date_year': '0'
        }
        
        form = TestForm(data)
        is_valid = form.is_valid()
        
        # Zero values should be handled gracefully (this might be less relevant
        # since 0 values are already handled in the original catch ValueError case)
        # But we test it to ensure consistent behavior
        try:
            if not is_valid:
                widget_value = form.fields['my_date'].widget.value_from_datadict(
                    data, {}, 'my_date'
                )
                # This should not raise an OverflowError
                self.assertIn("0", widget_value)
        except OverflowError:
            self.fail("OverflowError was raised with zero values")