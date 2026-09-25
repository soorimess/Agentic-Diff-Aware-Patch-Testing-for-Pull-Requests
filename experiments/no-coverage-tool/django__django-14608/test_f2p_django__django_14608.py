import sys
import os
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    settings.configure(
        USE_I18N=True,
        USE_L10N=True,
        SECRET_KEY='test-secret-key',
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sites',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'django.contrib.admindocs',
        ],
    )
    django.setup()

import unittest
from django.forms import Form, formset_factory, BaseFormSet
from django.core.exceptions import ValidationError


class TestForm(Form):
    name = 'test'


class CustomFormSet(BaseFormSet):
    def clean(self):
        # Raise a validation error that would go into non_form_errors
        raise ValidationError('Test non-form error')


class TestFormSetNonFormErrorsCSSClass(unittest.TestCase):
    def test_non_form_errors_get_nonform_css_class(self):
        """
        Test that non-form errors in formsets get the 'nonform' CSS class.
        This addresses the issue where FormSets should add 'nonform' CSS class
        for non-form errors, similar to how Forms add 'nonfield' CSS class for
        non-field errors.
        """
        # Create formset with custom formset that raises validation error in clean
        FormSet = formset_factory(TestForm, formset=CustomFormSet)
        formset = FormSet(data={})
        
        # Access non_form_errors which should create the error list with CSS class
        non_form_errors = formset.non_form_errors()
        
        # Check that the error list has the correct CSS class
        self.assertEqual(non_form_errors.error_class, 'errorlist nonform')


if __name__ == '__main__':
    unittest.main()