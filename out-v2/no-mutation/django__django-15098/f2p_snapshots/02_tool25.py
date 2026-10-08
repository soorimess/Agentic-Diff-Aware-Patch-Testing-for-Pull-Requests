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
        
        # Test cases that should match with the old regex (1 component max)
        old_style_cases = [
            '/en-us/',      # language-region
            '/en-US/',      # language-REGION
            '/en-latn/',    # language-script
        ]
        
        # Test cases that should match with the new regex (2 components max)
        new_style_cases = [
            '/en-latn-us/',   # language-script-region
            '/en-Latn-US/',   # language-SCRIPT-REGION
        ]
        
        # Test old-style cases (should work with both versions)
        for path in old_style_cases:
            match = language_code_prefix_re.match(path)
            self.assertIsNotNone(match, f"Regex should match old-style path: {path}")
            extracted_lang = match.group(1)
            expected_lang = path[1:-1] if path.endswith('/') else path[1:]
            self.assertEqual(extracted_lang, expected_lang, 
                           f"Regex should extract correct language code from: {path}")
        
        # Test new-style cases (should only work with the new regex)
        for path in new_style_cases:
            match = language_code_prefix_re.match(path)
            self.assertIsNotNone(match, f"Regex should match new-style path: {path}")
            extracted_lang = match.group(1)
            expected_lang = path[1:-1] if path.endswith('/') else path[1:]
            self.assertEqual(extracted_lang, expected_lang, 
                           f"Regex should extract correct language code from: {path}")

    @override_settings(
        USE_I18N=True,
        LANGUAGE_CODE='en-us',
        LANGUAGES=[
            ('en-us', "English"),
            ('en-latn-us', "Latin English"),
            ('en-Latn-US', "BCP 47 case format"),
            ('en-latn', "Latin English (no region)"),
        ],
        MIDDLEWARE=[
            'django.middleware.locale.LocaleMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ],
    )
    def test_edge_cases(self):
        """Test edge cases for language code parsing."""
        from django.utils.translation.trans_real import get_language_from_path
        
        # Test that valid language codes are properly parsed
        test_cases = [
            ('/en-us/', 'en-us'),
            ('/en-latn-us/', 'en-latn-us'),
            ('/en-Latn-US/', 'en-Latn-US'),
            ('/en-latn/', 'en-latn'),
        ]
        
        for path, expected_lang in test_cases:
            lang = get_language_from_path(path)
            self.assertEqual(lang, expected_lang, 
                           f"Language detection should work for: {path}")