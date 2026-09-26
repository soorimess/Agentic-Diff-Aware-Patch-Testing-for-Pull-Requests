from django import forms
from django.forms import SelectDateWidget
from django.test import TestCase


class SelectDateWidgetOverflowErrorTest(TestCase):
    """Test that SelectDateWidget handles OverflowError gracefully."""

    def test_select_date_widget_overflow_error(self):
        """Test that large integers in date fields don't cause OverflowError."""
        # Create a form with SelectDateWidget
        class ReproForm(forms.Form):
            my_date = forms.DateField(widget=SelectDateWidget())
        
        # Test case that would cause OverflowError before the fix
        # This should return "0-0-0" instead of raising OverflowError
        form = ReproForm({
            'my_date_day': '1',
            'my_date_month': '1', 
            'my_date_year': '1234567821345678',  # Large number that causes OverflowError
        })
        
        # The form should not raise OverflowError
        # Instead it should return "0-0-0" as per the fix
        result = form.fields['my_date'].widget.value_from_datadict(
            form.data, {}, 'my_date'
        )
        
        # Before the fix, this would raise OverflowError
        # After the fix, this should return "0-0-0"
        self.assertEqual(result, "0-0-0")