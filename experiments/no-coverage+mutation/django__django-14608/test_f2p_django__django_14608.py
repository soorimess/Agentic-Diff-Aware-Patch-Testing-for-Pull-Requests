"""
Regression test for Django ticket #14608: Add `nonform` CSS class for non form errors in FormSets.
This test ensures that non-form errors in FormSets have the 'nonform' CSS class
when using ErrorList instances.
"""
from django.core.exceptions import ValidationError
from django.forms import Form, formset_factory
from django.forms.formsets import BaseFormSet
from django.forms.utils import ErrorList
from django.test import SimpleTestCase


class TestForm(Form):
    name = 'test'


class TestFormSet(BaseFormSet):
    form = TestForm


class Django14608TestCase(SimpleTestCase):
    def test_non_form_errors_from_clean_method_have_nonform_css_class(self):
        """Test that non-form errors from FormSet.clean() have the 'nonform' CSS class."""
        # Create formset with non-form errors using clean() method
        class FormSetWithNonFormErrors(TestFormSet):
            def clean(self):
                raise ValidationError('This is a non-form error')
        
        FormSetWithErrors = formset_factory(TestForm, formset=FormSetWithNonFormErrors, extra=1, can_delete=False)
        
        # Create formset with data that will trigger a clean() error
        formset_with_errors = FormSetWithErrors(data={
            'form-0-name': 'test',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
        })
        
        # Call full_clean to trigger validation
        formset_with_errors.full_clean()
        
        # Get the non-form errors and check the CSS class
        non_form_errors = formset_with_errors.non_form_errors()
        
        # The error class should include 'nonform' after the fix
        self.assertIsInstance(non_form_errors, ErrorList)
        self.assertIn('nonform', getattr(non_form_errors, 'error_class', ''))
    
    def test_non_form_errors_from_management_form_have_nonform_css_class(self):
        """Test that non-form errors from management form issues have the 'nonform' CSS class."""
        # Create formset with missing management form 
        class EmptyFormSet(TestFormSet):
            form = TestForm

        FormSet = formset_factory(TestForm, formset=EmptyFormSet, extra=1, can_delete=False)
        
        # This will cause missing management form errors - should also have correct CSS
        formset = FormSet(data={'form-TOTAL_FORMS': '1'})
        
        formset.full_clean()
        non_form_errors = formset.non_form_errors()
        
        # The error class should include 'nonform' after the fix
        self.assertIsInstance(non_form_errors, ErrorList)
        self.assertIn('nonform', getattr(non_form_errors, 'error_class', ''))