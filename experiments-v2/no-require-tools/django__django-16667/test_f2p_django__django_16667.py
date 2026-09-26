from django import forms
from django.forms import SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowErrorTest(TestCase):
    def test_select_date_widget_overflow_error(self):
        """
        Test that SelectDateWidget handles OverflowError gracefully when
        large integers are passed as date components.
        """
        # Create a form with SelectDateWidget
        class ReproForm(forms.Form):
            my_date = forms.DateField(widget=SelectDateWidget())
        
        # Test case that would cause OverflowError with the old code
        # Large year value that would cause OverflowError when converted to int
        data = {
            'my_date_day': '1',
            'my_date_month': '1', 
            'my_date_year': '1234567821345678'  # Large number that causes OverflowError
        }
        
        form = ReproForm(data)
        
        # Check that the value_from_datadict returns "0-0-0" instead of raising OverflowError
        widget = form.fields['my_date'].widget
        result = widget.value_from_datadict(data, {}, 'my_date')
        self.assertEqual(result, "0-0-0")