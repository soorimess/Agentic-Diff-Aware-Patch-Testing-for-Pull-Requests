from django.test import SimpleTestCase, override_settings


class Django15098Tests(SimpleTestCase):
    @override_settings(
        USE_I18N=True,
        LANGUAGES=[
            ("en-us", "English"),
            ("en-latn-us", "Latin English"),
            ("en-Latn-US", "BCP 47 case format"),
        ],
    )
    def test_get_language_from_path_with_script_and_region(self):
        """
        get_language_from_path() should recognize language tags containing both
        script and region (e.g. "en-latn-us" and "en-Latn-US").
        """
        from django.utils import translation

        g = translation.trans_real.get_language_from_path
        self.assertEqual(g('/en-us/'), 'en-us')
        self.assertEqual(g('/en-latn-us/'), 'en-latn-us')
        self.assertEqual(g('/en-Latn-US/'), 'en-Latn-US')
