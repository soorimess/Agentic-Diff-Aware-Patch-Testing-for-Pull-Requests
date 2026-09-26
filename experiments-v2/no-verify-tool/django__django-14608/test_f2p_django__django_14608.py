from django import forms
from django.forms.formsets import BaseFormSet, formset_factory
from django.test import TestCase
from django.core.exceptions import ValidationError


class NonFormErrorFormSet(BaseFormSet):
    def clean(self):
        # Raise a validation error that should appear as a non-form error
        raise ValidationError('This is a non-form error')


class TestFormSetNonFormErrorCSSClass(TestCase):
    def test_non_form_errors_get_nonform_css_class(self):
        """Test that non-form errors in formsets get the 'nonform' CSS class."""
        # Create a formset that will have non-form errors
        FormSet = formset_factory(forms.Form, formset=NonFormErrorFormSet, extra=1)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-0-field': 'test',
        }
        
        formset = FormSet(data)
        
        # The formset should be invalid due to the non-form error
        self.assertFalse(formset.is_valid())
        
        # Check that non_form_errors has the correct CSS class
        non_form_errors = formset.non_form_errors()
        # The error list should have the 'nonform' CSS class
        # This is the key assertion - we need to check the error_class attribute
        self.assertEqual(len(non_form_errors), 1)
        self.assertEqual(non_form_errors[0], 'This is a non-form error')
        
        # Check that the error_class attribute of the ErrorList contains 'nonform'
        # This is what the change ensures
        self.assertIn('nonform', non_form_errors.error_class)
        self.assertIn('errorlist', non_form_errors.error_class)