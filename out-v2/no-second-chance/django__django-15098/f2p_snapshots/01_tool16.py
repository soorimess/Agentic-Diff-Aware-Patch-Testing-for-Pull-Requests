import os
import sys
from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.test.client import RequestFactory
from django.urls import path as django_path
from django.http import HttpResponse
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import get_language_from_path


# Set up settings for testing
@override_settings(
    USE_I18N=True,
    LANGUAGE_CODE='en-us',
    LANGUAGES=[
        ('en-us', "English"),
        ('en-latn-us', "Latin English"),
        ('en-Latn-US', "BCP 47 case format"),
    ],
    MIDDLEWARE=[
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
    ],
)
class I18nLanguageCodeTest(SimpleTestCase):
    """
    Test that i18n_patterns works with language codes containing both script and region.
    This is a regression test for Django ticket #15098.
    """
    
    def test_get_language_from_path_with_script_and_region(self):
        """
        Test that get_language_from_path correctly handles language codes
        with both script and region components like 'en-latn-us' and 'en-Latn-US'.
        """
        # Test cases that should work with the fixed version
        test_cases = [
            '/en-us/',           # Standard language code
            '/en-latn-us/',      # Language with script and region (lowercase)
            '/en-Latn-US/',      # Language with script and region (mixed case)
        ]
        
        # These should all return valid language codes
        for path in test_cases:
            lang_code = get_language_from_path(path)
            self.assertIsNotNone(lang_code, f"Failed to extract language code from {path}")
            
        # Test that specific language codes are correctly identified
        self.assertEqual(get_language_from_path('/en-latn-us/'), 'en-latn-us')
        self.assertEqual(get_language_from_path('/en-Latn-US/'), 'en-Latn-US')
        self.assertEqual(get_language_from_path('/en-us/'), 'en-us')
    
    def test_language_code_regex_pattern(self):
        """
        Direct test of the regex pattern that was changed in the fix.
        """
        # Test the specific regex behavior that was broken
        # The old regex r'^/(\w+([@-]\w+)?)(/|$)' only matches 1 additional component
        # The new regex r'^/(\w+([@-]\w+){0,2})(/|$)' matches up to 2 additional components
        
        # These should work with the fixed version but not with the old version
        test_paths = [
            '/en-latn-us/',      # 3 components: en-latn-us
            '/en-Latn-US/',      # 3 components: en-Latn-US
        ]
        
        for path in test_paths:
            lang_code = get_language_from_path(path)
            # With the old regex, this would return None
            # With the new regex, this should return the language code
            self.assertIsNotNone(lang_code, f"Language code not extracted from {path}")