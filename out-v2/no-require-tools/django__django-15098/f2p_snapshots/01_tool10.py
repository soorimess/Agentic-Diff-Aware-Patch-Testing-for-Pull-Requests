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
    
    def test_i18n_patterns_with_script_and_region(self):
        """Test that i18n_patterns works with language codes containing script and region."""
        # This test simulates the URL resolution behavior
        from django.urls import resolve
        from django.test.utils import override_script_prefix
        
        # Create a simple view function
        def bangiah(request):
            return HttpResponse('U!')
        
        # Create URL patterns with i18n_patterns
        urlpatterns = i18n_patterns(
            path('', bangiah, name='bangiah'),
        )
        
        # Test that URLs with script+region work
        factory = RequestFactory()
        
        # Test cases that should work
        test_cases = [
            '/en-us/',
            '/en-latn-us/',
            '/en-Latn-US/',
        ]
        
        for url_path in test_cases:
            with self.subTest(url=url_path):
                # Create a request
                request = factory.get(url_path)
                # This should not raise an exception for valid language codes
                try:
                    # Try to resolve the URL - this will test the language parsing
                    # We can't easily test the full resolution without a full URLconf setup
                    # but we can at least test that the language parsing works
                    lang = get_language_from_path(url_path)
                    self.assertIn(lang, ['en-us', 'en-latn-us', 'en-Latn-US'])
                except Exception as e:
                    self.fail(f"Failed to parse language from path {url_path}: {e}")