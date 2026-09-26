import unittest
from django.forms import Form, CharField, formset_factory
from django.forms.formsets import BaseFormSet
from django.core.exceptions import ValidationError


class TestFormSetNonFormErrorsCSSClass(unittest.TestCase):
    """Test that non-form errors in FormSets get the 'nonform' CSS class."""

    def test_non_form_errors_get_nonform_css_class(self):
        """Test that non-form errors in formsets have 'nonform' CSS class."""
        
        class TestForm(Form):
            field1 = CharField()
        
        class TestFormSet(BaseFormSet):
            def clean(self):
                # Raise a validation error that should appear as a non-form error
                raise ValidationError('This is a non-form error')
        
        # Create a formset with the custom clean method
        FormSet = formset_factory(
            form=TestForm, 
            formset=TestFormSet,
            extra=2
        )
        
        # Create formset with data that will trigger the validation error
        formset = FormSet(data={
            'form-0-field1': 'value1',
            'form-1-field1': 'value2',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
        })
        
        # Check that non_form_errors has the correct CSS class
        non_form_errors = formset.non_form_errors()
        
        # The error list should have 'nonform' as its CSS class
        self.assertEqual(non_form_errors.error_class, 'errorlist nonform')