from django.test import SimpleTestCase, override_settings
from django.utils import translation
from django.utils.translation import trans_real


class TestLanguageLocaleWithScriptAndRegion(SimpleTestCase):
    @override_settings(
        LANGUAGE_CODE='en-us',
        LANGUAGES=[
            ('en-us', 'English'),
            ('en-latn-us', 'Latin English'),
            ('en-Latn-US', 'BCP 47 case format'),
        ],
    )
    def test_get_language_from_path_with_script_and_region(self):
        """Language tags containing both script and region should be recognised.

        Regression test for bug where language locales with both script and
        region (e.g. "en-latn-us") were not recognised by get_language_from_path
        because the language-code prefix regexp only allowed a single
        subtag after the primary language.
        """
        g = trans_real.get_language_from_path
        # plain 2-part language still works
        self.assertEqual(g('/en-us/'), 'en-us')
        # language containing both script and region should be recognised
        self.assertEqual(g('/en-latn-us/'), 'en-latn-us')
        # and the BCP47-cased variant should also be recognised
        self.assertEqual(g('/en-Latn-US/'), 'en-Latn-US')
