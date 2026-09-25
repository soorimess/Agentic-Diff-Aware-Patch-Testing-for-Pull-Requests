"""
Regression test for Django issue #14608: 
Add `nonform` CSS class for non form errors in FormSets

Tests that non-form errors in FormSets have the CSS class "nonform" applied,
consistent with how non-field errors in Forms have CSS class "nonfield".
"""
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet, CharField, Form, formset_factory
from django.forms.utils import ErrorList
from django.test import SimpleTestCase


class TestForm(Form):
    name = CharField()


class TestFormSet(BaseFormSet):
    def clean(self):
        # This should produce a non-form error
        raise ValidationError('This is a formset-wide validation error')


TestFormSetFactory = formset_factory(TestForm, formset=TestFormSet, extra=1)


class FormSetNonFormErrorsCSSClassTests(SimpleTestCase):
    def test_non_form_errors_get_nonform_css_class(self):
        """Test that non-form errors in formsets have 'nonform' CSS class."""
        # Create a formset that will have non-form errors
        formset = TestFormSetFactory(data={}, auto_id=False)
        
        # Trigger validation to populate _non_form_errors
        is_valid = formset.is_valid()
        
        # The formset should be invalid
        self.assertFalse(is_valid)
        
        # Check the error list has the error
        non_form_errors = formset.non_form_errors()
        self.assertEqual(len(non_form_errors), 1)
        self.assertEqual(non_form_errors[0], 'This is a formset-wide validation error')
        
        # Test that the non_form_errors ErrorList uses the "nonform" CSS class
        # This requires looking at the internal _non_form_errors attribute 
        # and checking its error_class attribute
        error_list = formset._non_form_errors
        self.assertIsInstance(error_list, ErrorList)
        
        # Before the fix: error_class would be just "errorlist"
        # After the fix: error_class should be "errorlist nonform"
        self.assertIn('nonform', error_list.error_class)