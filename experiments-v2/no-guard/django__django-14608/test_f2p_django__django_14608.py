"""
Regression test for Django ticket #14608: Add `nonform` CSS class for non form errors in FormSets.

This test ensures that when a formset has non-form errors (errors from the formset's clean() method),
those errors get the CSS class 'nonform' applied to them, just like how form errors get 'nonfield' class.
"""
import unittest
from django.forms import BaseFormSet
from django.forms.formsets import formset_factory


class TestNonFormErrorCSSClass(unittest.TestCase):
    def test_non_form_errors_get_nonform_css_class(self):
        """
        Test that non-form errors in formsets have 'nonform' CSS class.
        
        This test verifies the fix that adds error_class='nonform' to ErrorList 
        instances for non-form errors in formsets, similar to how forms have 
        error_class='nonfield' for non-field errors.
        """
        # Test the initialization path - this covers line 336 in formsets.py
        class TestFormSet(BaseFormSet):
            pass
        
        FormSet = formset_factory(TestFormSet, extra=0)
        formset = FormSet()
        
        # Access non_form_errors to trigger full_clean which initializes _non_form_errors
        # After the fix, this should initialize with error_class='nonform'
        non_form_errors = formset.non_form_errors()
        
        # The ErrorList should have 'nonform' CSS class
        # Before the fix: error_class = 'errorlist' 
        # After the fix: error_class = 'errorlist nonform'
        self.assertIn('nonform', non_form_errors.error_class)