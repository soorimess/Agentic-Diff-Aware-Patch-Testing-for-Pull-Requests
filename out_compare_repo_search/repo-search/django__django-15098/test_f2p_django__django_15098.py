from django.test import SimpleTestCase, override_settings
from django.utils.translation import get_language_from_path


class GetLanguageFromPathTests(SimpleTestCase):
    @override_settings(
        LANGUAGES=[
            ("en-us", "English"),
            ("en-latn-us", "Latin English"),
            ("en-Latn-US", "BCP 47 case format"),
        ],
    )
    def test_language_with_script_and_region_in_path(self):
        # Basic two-part language still recognised
        self.assertEqual(get_language_from_path('/en-us/'), 'en-us')
        # Languages with both script and region should be recognised
        self.assertIsNotNone(get_language_from_path('/en-latn-us/'))
        # BCP 47 case variants should also be recognised
        self.assertIsNotNone(get_language_from_path('/en-Latn-US/'))
