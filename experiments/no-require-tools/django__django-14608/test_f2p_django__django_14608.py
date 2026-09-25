from django.core.exceptions import ValidationError
from django.forms import BaseFormSet, Form
from django.forms.formsets import formset_factory
from django.forms.utils import ErrorList
from django.test import SimpleTestCase


class TestForm(Form):
    name = 'test'


class TestFormSet(BaseFormSet):
    form = TestForm
    extra = 1

    def clean(self):
        raise ValidationError('Formset validation error')


class NonFormErrorsCSSTests(SimpleTestCase):
    """Tests for CSS class on non-form errors in formsets."""

    def test_non_form_errors_get_nonform_css_class(self):
        """Test that non-form errors in formsets have 'nonform' CSS class."""
        # Create a formset factory with our custom formset class
        FormSet = formset_factory(TestForm, formset=TestFormSet, extra=1)
        
        # Create formset instance
        formset = FormSet()
        
        # Call full_clean which should populate _non_form_errors
        formset.full_clean()
        
        # The error_class should be 'nonform' for non-form errors
        self.assertEqual(formset._non_form_errors.error_class, 'nonform')

    def test_non_form_errors_via_error_class_parameter(self):
        """Test that non-form errors use error_class parameter when created."""
        # Test case from the diff: error_class should be passed when creating _non_form_errors
        FormSet = formset_factory(TestForm, formset=TestFormSet, extra=1)
        formset = FormSet()
        
        # Trigger the clean that would raise a validation error 
        formset.full_clean()
        
        # Verify that the error list is correctly instantiated with error_class='nonform'
        # Check what error_class was passed to the ErrorList constructor
        self.assertEqual(
            getattr(formset._non_form_errors, 'error_class', None), 
            'nonform'
        )
