import os
import sys
from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.test.client import RequestFactory
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse
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
    ROOT_URLCONF='test_urls',
)
class I18nLanguageCodeTest(SimpleTestCase):
    """Test for i18n patterns with language codes containing both script and region."""
    
    def test_get_language_from_path_with_script_and_region(self):
        """Test that get_language_from_path works with language codes containing script and region."""
        # Test cases for language codes with script and region
        test_cases = [
            ('/en-us/', 'en-us'),
            ('/en-latn-us/', 'en-latn-us'),
            ('/en-Latn-US/', 'en-Latn-US'),
        ]
        
        for path_input, expected_language in test_cases:
            with self.subTest(path=path_input):
                result = get_language_from_path(path_input)
                self.assertEqual(result, expected_language, 
                               f"Expected {expected_language} for path {path_input}, got {result}")
    
    def test_language_code_parsing(self):
        """
        Test that language codes with script and region are properly parsed.
        This directly tests the regex behavior that was fixed.
        """
        # The core issue was that get_language_from_path returned None for 
        # language codes with both script and region components
        test_cases = [
            '/en-us/',           # Should work - basic language
            '/en-latn-us/',      # Should work - script + region (the bug case)
            '/en-Latn-US/',      # Should work - BCP 47 case format (the bug case)
        ]
        
        for path_input in test_cases:
            with self.subTest(path=path_input):
                lang = get_language_from_path(path_input)
                # All these should return a language code, not None
                self.assertIsNotNone(lang, f"Language code should be parsed from {path_input}")
                self.assertIn(lang, ['en-us', 'en-latn-us', 'en-Latn-US'])