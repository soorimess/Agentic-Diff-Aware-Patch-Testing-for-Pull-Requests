import unittest
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet, formset_factory
from django.forms.utils import ErrorList


class NonFormErrorFormSet(BaseFormSet):
    def clean(self):
        # Raise a non-form validation error to test the exception path
        raise ValidationError('This is a non-form error')


class TestNonFormErrorCSSClass(unittest.TestCase):
    
    def test_non_form_errors_get_nonform_css_class(self):
        """Test that non-form errors in formsets get the 'nonform' CSS class."""
        FormSet = formset_factory(NonFormErrorFormSet, extra=2)
        formset = FormSet()
        
        # This should trigger the clean() method and create non-form errors
        formset.full_clean()
        
        # Check that the non-form errors have the 'nonform' CSS class
        self.assertIsInstance(formset._non_form_errors, ErrorList)
        self.assertIn('nonform', formset._non_form_errors.error_class)
        
    def test_non_form_errors_from_management_form(self):
        """Test that management form errors also get the 'nonform' CSS class."""
        FormSet = formset_factory(NonFormErrorFormSet, extra=2)
        # Create a formset with invalid management form data
        formset = FormSet(data={'form-TOTAL_FORMS': 'invalid', 'form-INITIAL_FORMS': '0'})
        
        formset.full_clean()
        
        # Check that the non-form errors have the 'nonform' CSS class
        self.assertIsInstance(formset._non_form_errors, ErrorList)
        self.assertIn('nonform', formset._non_form_errors.error_class)