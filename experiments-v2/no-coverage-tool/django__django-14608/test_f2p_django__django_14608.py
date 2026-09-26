import unittest
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet, Form, CharField, formset_factory


class TestFormSetNonFormErrors(unittest.TestCase):
    """Test that FormSets use 'nonform' CSS class for non-form errors."""

    def test_non_form_errors_use_nonform_css_class(self):
        """Test that non-form errors in formsets have 'nonform' CSS class."""
        
        # Create a simple form class
        class TestForm(Form):
            name = CharField()
        
        # Create a formset that raises a ValidationError in clean()
        class TestFormSet(BaseFormSet):
            def clean(self):
                raise ValidationError("This is a non-form error")
        
        # Create a formset factory
        TestFormSetFactory = formset_factory(TestForm, formset=TestFormSet, extra=1)
        
        # Create formset with data
        formset = TestFormSetFactory(data={'form-0-name': 'test'})
        
        # Clean the formset to trigger the ValidationError
        formset.full_clean()
        
        # Get the non-form errors
        non_form_errors = formset.non_form_errors()
        
        # Check that the error list has the correct CSS class
        # The error_class should be 'errorlist nonform' for non-form errors
        self.assertEqual(non_form_errors.error_class, 'errorlist nonform')