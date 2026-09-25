"""
Regression test for Django issue #14608:
Add `nonform` CSS class for non form errors in FormSets
"""
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet, Form, formset_factory
from django.test import SimpleTestCase


class TestNonFormCssClass(SimpleTestCase):
    """Test that non-form errors in formsets have the 'nonform' CSS class."""

    def test_nonform_css_class_in_formsets(self):
        """
        Test that non-form errors in formsets have the 'nonform' CSS class.
        
        This verifies the fix for Django issue #14608 where non-form errors in 
        formsets should have the 'nonform' CSS class to differentiate them from 
        non-field errors in forms.
        """
        # Create a formset that raises a validation error
        class CustomFormSet(BaseFormSet):
            def clean(self):
                # Trigger a non-form error by raising ValidationError
                raise ValidationError("Custom non-form error")

        # Create a formset with our custom error list
        FormSet = formset_factory(Form, formset=CustomFormSet, extra=0)
        
        # Create formset instance 
        formset = FormSet(data={})
        
        # Perform validation to trigger the error handling path
        formset.full_clean()
        
        # Check that non_form_errors has the correct CSS class
        # The _non_form_errors should have been created with error_class='nonform'
        expected_error_class = "errorlist nonform"
        actual_error_class = formset._non_form_errors.error_class
        self.assertEqual(actual_error_class, expected_error_class)

    def test_nonform_css_class_on_validation_error(self):
        """
        Test that non-form errors from ValidationError exceptions get 'nonform' CSS class.
        
        This specifically tests the second scenario in the diff:
        self._non_form_errors = self.error_class(e.error_list, error_class='nonform')
        """
        class CustomFormSet(BaseFormSet):
            def clean(self):
                # This should trigger the exception path that creates _non_form_errors
                raise ValidationError("Validation error in formset")

        FormSet = formset_factory(Form, formset=CustomFormSet, extra=0)
        formset = FormSet(data={})
        
        # Trigger validation - this will cause clean() to be called and Exception to be caught
        formset.full_clean()
        
        # Check that the error list has the correct CSS class
        expected_error_class = "errorlist nonform"
        actual_error_class = formset._non_form_errors.error_class
        self.assertEqual(actual_error_class, expected_error_class)