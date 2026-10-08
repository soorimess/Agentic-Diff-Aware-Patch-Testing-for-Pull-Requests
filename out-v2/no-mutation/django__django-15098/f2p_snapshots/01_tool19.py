import os
import sys

from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.test.client import RequestFactory
from django.urls import path, reverse
from django.http import HttpResponse

from django.conf.urls.i18n import i18n_patterns


def bangiah(request):
    return HttpResponse('U!')


class I18nScriptRegionTest(SimpleTestCase):
    """Test that i18n_patterns works with language codes containing both script and region."""

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
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ],
    )
    def test_language_code_with_script_and_region(self):
        """Test that en-latn-us and en-Latn-US work with i18n_patterns."""
        # Test the language detection directly
        from django.utils.translation.trans_real import get_language_from_path
        from django.utils.translation.trans_real import language_code_prefix_re
        
        # This should work - standard language code
        lang = get_language_from_path('/en-us/')
        self.assertEqual(lang, 'en-us')
        
        # These should work but currently don't due to the regex bug
        lang = get_language_from_path('/en-latn-us/')
        self.assertEqual(lang, 'en-latn-us')
        
        lang = get_language_from_path('/en-Latn-US/')
        self.assertEqual(lang, 'en-Latn-US')

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
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ],
    )
    def test_regex_matching_for_script_region_codes(self):
        """Test that the regex correctly matches language codes with script and region."""
        from django.utils.translation.trans_real import language_code_prefix_re
        
        # Test cases that should match
        test_cases = [
            '/en-us/',
            '/en-latn-us/',
            '/en-Latn-US/',
        ]
        
        for path in test_cases:
            match = language_code_prefix_re.match(path)
            self.assertIsNotNone(match, f"Regex should match path: {path}")
            # The first group should be the language code
            extracted_lang = match.group(1)
            # For paths like /en-latn-us/, the language code should be en-latn-us
            expected_lang = path[1:-1] if path.endswith('/') else path[1:]
            self.assertEqual(extracted_lang, expected_lang, 
                           f"Regex should extract correct language code from: {path}")