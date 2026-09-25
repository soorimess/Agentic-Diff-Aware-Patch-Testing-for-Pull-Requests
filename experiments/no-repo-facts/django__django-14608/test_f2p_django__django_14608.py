"""
Test for Django issue #14608: Add `nonform` CSS class for non form errors in FormSets

This test verifies that formset non-form errors have the 'nonform' CSS class 
applied to their ErrorList, consistent with how form non-field errors get the 'nonfield' class.
"""
from django.core.exceptions import ValidationError
from django.forms import BaseForm, Form, CharField, formset_factory
from django.forms.formsets import BaseFormSet
from django.test import SimpleTestCase


class TestForm(Form):
    name = CharField(max_length=100)


class CustomFormSet(BaseFormSet):
    def clean(self):
        # Raise a non-form validation error
        raise ValidationError('This is a formset-level error')


TestFormSet = formset_factory(TestForm, formset=CustomFormSet, extra=1)


class TestNonFormErrorsCSSClass(SimpleTestCase):
    def test_non_form_errors_get_nonform_css_class(self):
        """
        Test that non-form errors in formsets get 'nonform' CSS class.
        """
        # Create a formset that will trigger non-form validation error
        formset = TestFormSet(data={
            'form-0-name': 'test',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
        })
        
        # Check that clean() raises ValidationError and 
        # non_form_errors have proper CSS class
        self.assertFalse(formset.is_valid())
        
        # Get the non-form errors
        non_form_errors = formset.non_form_errors()
        
        # This assertion should pass after the fix is applied
        # Before the fix, error_class would be 'errorlist'
        # After the fix, error_class should be 'errorlist nonform'
        self.assertEqual(non_form_errors.error_class, 'errorlist nonform')
        
    def test_non_form_errors_empty_has_correct_css_class(self):
        """
        Test that empty non-form errors also correctly have the 'nonform' CSS class.
        """
        # Create an empty formset without errors  
        formset = TestFormSet(data={
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0', 
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
        })
        
        # Even empty non_form_errors should have the correct class
        non_form_errors = formset.non_form_errors()
        
        # Should have the 'nonform' CSS class
        self.assertEqual(non_form_errors.error_class, 'errorlist nonform')