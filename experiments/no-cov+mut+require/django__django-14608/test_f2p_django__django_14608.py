import unittest
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet, Form, formset_factory
from django.forms.utils import ErrorList


class NonFormErrorClassFormSet(BaseFormSet):
    def clean(self):
        # Raise a non-form error to test the CSS class
        raise ValidationError('Non-form error message')


class FormSetErrorClassTests(unittest.TestCase):
    def test_non_form_errors_get_nonform_css_class(self):
        """
        Test that non-form errors in FormSets get the 'nonform' CSS class.
        """
        FormSet = formset_factory(Form, formset=NonFormErrorClassFormSet, extra=1)
        formset = FormSet()

        # This should trigger non-form errors
        formset.full_clean()

        # Check that non-form errors have 'nonform' CSS class
        # The error_class attribute has the format "errorlist nonform" when nonform is present
        self.assertEqual(formset.non_form_errors().error_class, 'errorlist nonform')

    def test_non_form_errors_from_validation_error_with_list(self):
        """
        Test that non-form errors from ValidationError error_list also get the 'nonform' CSS class.
        """
        class ValidationErrorFormSet(BaseFormSet):
            def clean(self):
                raise ValidationError(['Error 1', 'Error 2'])

        FormSet = formset_factory(Form, formset=ValidationErrorFormSet, extra=1)
        formset = FormSet()

        # This should trigger non-form errors from ValidationError
        formset.full_clean()

        # Check that non-form errors have 'nonform' CSS class
        self.assertEqual(formset.non_form_errors().error_class, 'errorlist nonform')