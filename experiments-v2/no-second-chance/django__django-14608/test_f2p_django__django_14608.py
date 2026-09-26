import unittest
from django.forms import BaseFormSet, Form, CharField, formset_factory
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList


class NonFormErrorClassTest(unittest.TestCase):
    def test_non_form_errors_initial_creation_has_nonform_css_class(self):
        """Test that initial _non_form_errors gets 'nonform' CSS class."""
        
        class TestForm(Form):
            name = CharField()
        
        class TestFormSet(BaseFormSet):
            def clean(self):
                # This will not be called in this test case
                pass
        
        # Create a formset factory with our custom formset
        FormSet = formset_factory(
            form=TestForm,
            formset=TestFormSet,
            extra=1,
            max_num=1,
            validate_max=True
        )
        
        # Create a formset instance with invalid management form data
        # This should trigger the management form error path where _non_form_errors is created
        formset = FormSet(data={'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '0'})
        
        # Force full_clean to happen to ensure _non_form_errors is created
        formset.full_clean()
        
        # Check that the error list has the 'nonform' CSS class
        self.assertEqual(formset._non_form_errors.error_class, 'errorlist nonform')
    
    def test_non_form_errors_exception_creation_has_nonform_css_class(self):
        """Test that _non_form_errors from exceptions get 'nonform' CSS class."""
        
        class TestForm(Form):
            name = CharField()
        
        class TestFormSet(BaseFormSet):
            def clean(self):
                # This will be called and raise an exception
                raise ValidationError('Exception non-form error')
        
        # Create a formset factory with our custom formset
        FormSet = formset_factory(
            form=TestForm,
            formset=TestFormSet,
            extra=1,
            max_num=1,
            validate_max=True
        )
        
        # Create a formset instance
        formset = FormSet()
        
        # Force full_clean to happen to ensure _non_form_errors is created
        formset.full_clean()
        
        # Check that the error list has the 'nonform' CSS class
        self.assertEqual(formset._non_form_errors.error_class, 'errorlist nonform')