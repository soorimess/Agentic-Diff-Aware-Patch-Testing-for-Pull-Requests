"""
Regression test for Django issue #14608:
Add `nonform` CSS class for non form errors in FormSets

This test ensures that non-form errors in formsets get the 'nonform' CSS class,
similar to how non-field errors in forms get the 'nonfield' CSS class.
"""
import unittest
from django.forms import BaseFormSet, formset_factory, ValidationError
from django.forms.utils import ErrorList


class TestNonFormErrorCSSClass(unittest.TestCase):
    
    def test_non_form_errors_get_nonform_css_class(self):
        """
        Test that non-form errors in formsets get the 'nonform' CSS class.
        """
        # Create a formset with a custom formset that raises non-form errors
        class BaseCustomFormSet(BaseFormSet):
            def clean(self):
                raise ValidationError("This is a non-form error")

        # Create a simple form to use with the formset
        from django.forms import Form, CharField
        class Choice(Form):
            choice = CharField()

        ChoiceFormSet = formset_factory(Choice, formset=BaseCustomFormSet)
        
        # Create formset instance with data that will trigger validation
        data = {
            'choices-TOTAL_FORMS': '1',
            'choices-INITIAL_FORMS': '0',
        }
        formset = ChoiceFormSet(data, auto_id=False, prefix='choices')
        
        # Access non_form_errors to trigger full_clean and validation
        # This should trigger the ValidationError path in full_clean
        non_form_errors = formset.non_form_errors()
        
        # Check that we have the expected error
        self.assertEqual(len(non_form_errors), 1)
        # Check that the error list has the correct CSS class
        # This is the key assertion - the error_class should contain 'nonform'
        self.assertIn('nonform', non_form_errors.error_class)