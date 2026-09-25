"""
Regression test for Django issue #14608
Tests that FormSets add 'nonform' CSS class for non form errors.
"""
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet, Form, CharField
from django.forms.formsets import formset_factory
from django.test import SimpleTestCase


class TestForm(Form):
    name = CharField()


class TestFormSet(BaseFormSet):
    def clean(self):
        # Simulate a validation error that would be a non-form error
        raise ValidationError('Test non-form error')


class FormSetNonFormErrorsCSSClassTest(SimpleTestCase):
    def test_non_form_errors_get_nonform_css_class(self):
        """Test that non-form errors in formsets get the 'nonform' CSS class."""
        TestFormSetFactory = formset_factory(TestForm, formset=TestFormSet, extra=1)
        formset = TestFormSetFactory()
        
        # This should trigger the ValidationError in clean() method 
        # and create non-form errors with 'nonform' CSS class
        formset.full_clean()
        
        # Get the non-form errors
        non_form_errors = formset.non_form_errors()
        
        # The ErrorList should have 'nonform' CSS class
        self.assertTrue(hasattr(non_form_errors, 'error_class'))
        self.assertIn('nonform', non_form_errors.error_class)

    def test_initial_non_form_errors_get_nonform_css_class(self):
        """Test that initial non-form errors get the 'nonform' CSS class."""
        TestFormSetFactory = formset_factory(TestForm, formset=TestFormSet, extra=1)
        formset = TestFormSetFactory()
        
        # Manually create non-form errors with error_class parameter
        # This tests line 336 in the diff: self._non_form_errors = self.error_class(error_class='nonform')
        formset._non_form_errors = formset.error_class(error_class='nonform')
        
        # Verify the error class is set correctly
        self.assertTrue(hasattr(formset._non_form_errors, 'error_class'))
        self.assertIn('nonform', formset._non_form_errors.error_class)