from django.apps import apps
from django.test import TestCase


class AppsClearCacheSwappableSettingsNameTests(TestCase):
    """
    Regression test for Django ticket #17029 (get_swappable_settings_name cache
    should be cleared by Apps.clear_cache()).

    Before the fix, calling apps.clear_cache() did not clear the
    functools.cache on get_swappable_settings_name, so the cached value could
    survive changes to settings. This test ensures that clearing the apps
    registry also causes get_swappable_settings_name to be refreshed.
    """

    # Limit the apps involved to speed up the test and to ensure the
    # swappable_models app is available.
    available_apps = [
        "swappable_models",
        "django.contrib.auth",
        "django.contrib.contenttypes",
    ]

    def test_clear_cache_clears_get_swappable_settings_name(self):
        # Ensure any previous cache is cleared.
        apps.get_swappable_settings_name.cache_clear()

        # Prime the cache with a value dependent on a setting.
        with self.settings(TEST_ARTICLE_MODEL="swappable_models.AlternateArticle"):
            self.assertEqual(
                apps.get_swappable_settings_name("swappable_models.AlternateArticle"),
                "TEST_ARTICLE_MODEL",
            )

        # After settings are reverted, clear the apps registry cache. The
        # get_swappable_settings_name cache must be cleared as well so that a
        # subsequent call reflects the current settings (None).
        apps.clear_cache()
        self.assertIsNone(apps.get_swappable_settings_name("swappable_models.AlternateArticle"))
