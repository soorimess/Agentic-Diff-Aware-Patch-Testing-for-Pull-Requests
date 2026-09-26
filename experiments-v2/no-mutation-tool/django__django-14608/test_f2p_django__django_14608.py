"""
Regression test for Django issue #14608.

This test ensures that non-form errors in FormSets have the 'nonform' CSS class
added to their error_class attribute, matching the behavior of non-field errors
in Forms.
"""
import unittest
from django.forms import BaseFormSet, formset_factory, ValidationError
from django.forms.utils import ErrorList
from django.forms import Form, CharField


class Choice(Form):
    choice = CharField()


class BaseCustomFormSet(BaseFormSet):
    def clean(self):
        raise ValidationError("This is a non-form error")


class TestNonFormErrorCSSClass(unittest.TestCase):
    def test_non_form_errors_get_nonform_css_class(self):
        """
        Test that non-form errors in FormSets have 'nonform' CSS class.
        """
        # Create a formset with non-form errors using the same approach as existing tests
        ChoiceFormSet = formset_factory(Choice, formset=BaseCustomFormSet)
        data = {
            'choices-TOTAL_FORMS': '1',
            'choices-INITIAL_FORMS': '0',
        }
        formset = ChoiceFormSet(data, auto_id=False, prefix='choices')
        
        # Check that non_form_errors has the correct error_class
        non_form_errors = formset.non_form_errors()
        self.assertIsInstance(non_form_errors, ErrorList)
        
        # Before the fix, this would be 'errorlist'
        # After the fix, this should be 'errorlist nonform'
        self.assertEqual(non_form_errors.error_class, 'errorlist nonform')
        
    def test_non_form_errors_with_validation_error_list(self):
        """
        Test that non-form errors from ValidationError.error_list also get 'nonform' CSS class.
        """
        class CustomFormSet(BaseFormSet):
            def clean(self):
                raise ValidationError(["Error 1", "Error 2"])
        
        ChoiceFormSet = formset_factory(Choice, formset=CustomFormSet)
        data = {
            'choices-TOTAL_FORMS': '1',
            'choices-INITIAL_FORMS': '0',
        }
        formset = ChoiceFormSet(data, auto_id=False, prefix='choices')
        
        # Check that non_form_errors has the correct error_class
        non_form_errors = formset.non_form_errors()
        self.assertIsInstance(non_form_errors, ErrorList)
        
        # Before the fix, this would be 'errorlist'
        # After the fix, this should be 'errorlist nonform'
        self.assertEqual(non_form_errors.error_class, 'errorlist nonform')