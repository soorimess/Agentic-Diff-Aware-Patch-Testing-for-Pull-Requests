import os
import sys
from django.conf import settings
from django.test import SimpleTestCase, override_settings
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse


def bangiah(request):
    return HttpResponse('U!')


class I18nPatternsScriptRegionTest(SimpleTestCase):
    """Test that i18n_patterns works with language codes containing script and region."""
    
    @override_settings(
        USE_I18N=True,
        LANGUAGE_CODE='en-us',
        LANGUAGES=[
            ('en-us', "English"),
            ('en-latn-us', "Latin English"),
            ('en-Latn-US', "BCP 47 case format"),
        ],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        ROOT_URLCONF=__name__,
    )
    def test_language_code_with_script_and_region_lowercase(self):
        """Test that i18n_patterns works with lowercase language codes containing both script and region."""
        # This should return 200 for en-latn-us (lowercase)
        response = self.client.get('/en-latn-us/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'U!')

    @override_settings(
        USE_I18N=True,
        LANGUAGE_CODE='en-us',
        LANGUAGES=[
            ('en-us', "English"),
            ('en-latn-us', "Latin English"),
            ('en-Latn-US', "BCP 47 case format"),
        ],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        ROOT_URLCONF=__name__,
    )
    def test_language_code_with_script_and_region_mixed_case(self):
        """Test that i18n_patterns works with mixed case language codes containing both script and region."""
        # This should return 200 for en-Latn-US (mixed case - BCP 47 format)
        response = self.client.get('/en-Latn-US/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'U!')

    @override_settings(
        USE_I18N=True,
        LANGUAGE_CODE='en-us',
        LANGUAGES=[
            ('en-us', "English"),
        ],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        ROOT_URLCONF=__name__,
    )
    def test_language_code_with_only_region(self):
        """Test that i18n_patterns still works with language codes containing only region."""
        # Test that the basic functionality still works
        response = self.client.get('/en-us/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'U!')


# URL patterns for testing
urlpatterns = [
    path('', bangiah),
]
urlpatterns = i18n_patterns(*urlpatterns)