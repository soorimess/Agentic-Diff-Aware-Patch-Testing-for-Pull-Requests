"""
Test for Django issue #14608: Add `nonform` CSS class for non form errors in FormSets
"""
from django import forms
from django.forms import Form, formset_factory
from django.forms.formsets import BaseFormSet
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase


class TestForm(Form):
    name = forms.CharField()


class TestFormSet(BaseFormSet):
    def clean(self):
        # Simulate a formset-wide validation error
        raise ValidationError("Formset validation error")


TestFormSet = formset_factory(TestForm, formset=TestFormSet, extra=1)


class FormSetNonFormErrorsTest(SimpleTestCase):
    def test_non_form_errors_get_nonform_css_class(self):
        """Test that non-form errors in formsets get 'nonform' CSS class."""
        # Create a formset with validation error in clean()
        formset = TestFormSet(data={
            'form-0-name': 'test',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
        })
        
        # This should trigger a non-form error from clean() method
        formset.full_clean()
        
        # Check that non_form_errors has the correct CSS class
        non_form_errors = formset.non_form_errors()
        
        # The error should have 'nonform' class in its HTML representation
        error_html = str(non_form_errors)
        self.assertIn('nonform', error_html)
        self.assertIn('errorlist', error_html)  # Should still have the base class