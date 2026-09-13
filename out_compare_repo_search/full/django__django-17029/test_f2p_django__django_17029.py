from django.apps import apps
from django.test import SimpleTestCase


class GetSwappableSettingsNameCacheClearTests(SimpleTestCase):
    def tearDown(self):
        # Ensure we leave the global apps registry in a clean state.
        try:
            apps.unset_available_apps()
        except Exception:
            # If no available apps were set, ignore.
            pass
        apps.clear_cache()

    def test_clear_cache_clears_get_swappable_settings_name(self):
        # Prime the cache with a swappable model (the built-in auth.User).
        self.assertEqual(apps.get_swappable_settings_name("auth.user"), "AUTH_USER_MODEL")

        # Restrict available apps to a subset that doesn't include auth.
        apps.set_available_apps(["django.contrib.contenttypes"])
        try:
            # After restricting available apps, get_swappable_settings_name should
            # no longer find the auth.User model and must return None.
            self.assertIsNone(apps.get_swappable_settings_name("auth.user"))
        finally:
            apps.unset_available_apps()
