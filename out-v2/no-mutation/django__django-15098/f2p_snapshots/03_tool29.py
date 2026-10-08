from django.conf import settings
from django.test import SimpleTestCase, override_settings
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
        """Test that language codes with script and region work with i18n_patterns."""
        # Test the language detection directly - this is the core functionality that was broken
        from django.utils.translation.trans_real import get_language_from_path
        
        # Standard language code should work
        lang = get_language_from_path('/en-us/')
        self.assertEqual(lang, 'en-us')
        
        # Language codes with both script and region should work (this was broken before the fix)
        lang = get_language_from_path('/en-latn-us/')
        self.assertEqual(lang, 'en-latn-us')
        
        lang = get_language_from_path('/en-Latn-US/')
        self.assertEqual(lang, 'en-Latn-US')