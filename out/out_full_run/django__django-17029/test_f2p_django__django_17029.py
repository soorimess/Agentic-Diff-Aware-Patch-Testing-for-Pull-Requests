from django.apps import apps
from django.test import SimpleTestCase


class AppsClearCacheTests(SimpleTestCase):
    def test_clear_cache_clears_get_swappable_settings_name(self):
        """
        Ensure Apps.clear_cache() clears the lru cache used by
        get_swappable_settings_name. If it doesn't, a previously cached
        swappable setting (e.g. AUTH_USER_MODEL for auth.User) will still be
        returned even after restricting available apps.
        """
        # Prime the cache with the auth.User lookup.
        self.assertEqual(apps.get_swappable_settings_name("auth.User"), "AUTH_USER_MODEL")

        # Restrict available apps to everything except django.contrib.auth.
        available = [ac.name for ac in apps.get_app_configs() if ac.name != "django.contrib.auth"]
        apps.set_available_apps(available)
        try:
            # After clearing caches as part of set_available_apps(), the
            # swappable lookup for auth.User should no longer be present.
            # Before the bugfix, get_swappable_settings_name() would still
            # return the cached "AUTH_USER_MODEL" value here.
            self.assertIsNone(apps.get_swappable_settings_name("auth.User"))
        finally:
            # Restore the registry and ensure we don't leak cache state to
            # other tests.
            apps.unset_available_apps()
            try:
                apps.get_swappable_settings_name.cache_clear()
            except AttributeError:
                # If the cache machinery isn't present for some reason,
                # ignore the cleanup.
                pass
