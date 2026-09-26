import unittest
from django import forms
from django.forms.formsets import BaseFormSet, formset_factory
from django.core.exceptions import ValidationError


class TestForm(forms.Form):
    name = forms.CharField()


class TestFormSet(BaseFormSet):
    form = TestForm

    def clean(self):
        # Raise a validation error to trigger non-form errors
        raise ValidationError('This is a formset-level error')


class TestNonFormCssClass(unittest.TestCase):
    def test_nonform_css_class_in_formsets(self):
        """Test that formsets add 'nonform' CSS class for non-form errors."""
        # Create a formset that will have non-form errors
        TestFormSetFactory = formset_factory(TestForm, formset=TestFormSet, extra=1)
        formset = TestFormSetFactory(data={'form-0-name': 'test', 'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '0'})
        
        # This should trigger non-form errors via the clean() method
        self.assertFalse(formset.is_valid())
        
        # Get the non-form errors
        non_form_errors = formset.non_form_errors()
        
        # The error list should have the 'nonform' CSS class
        self.assertTrue(hasattr(non_form_errors, 'error_class'))
        self.assertIn('nonform', non_form_errors.error_class)
    
    def test_nonform_css_class_in_formsets_from_management_form(self):
        """Test that formsets add 'nonform' CSS class for management form errors."""
        TestFormSetFactory = formset_factory(TestForm, formset=TestFormSet, extra=1)
        # Create data that will cause management form validation to fail
        formset = TestFormSetFactory(data={'form-TOTAL_FORMS': 'invalid', 'form-INITIAL_FORMS': 'invalid'})
        
        # This should trigger non-form errors from management form validation
        self.assertFalse(formset.is_valid())
        
        # Get the non-form errors
        non_form_errors = formset.non_form_errors()
        
        # The error list should have the 'nonform' CSS class
        self.assertTrue(hasattr(non_form_errors, 'error_class'))
        self.assertIn('nonform', non_form_errors.error_class)