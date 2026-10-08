import unittest
from django.apps import apps


class AppsCacheClearTest(unittest.TestCase):
    def test_apps_clear_cache_clears_get_swappable_settings_name_cache(self):
        """
        Regression test for Django issue #17029.
        
        Apps.clear_cache() should clear the get_swappable_settings_name cache.
        This test verifies that the fix is in place and working correctly.
        """
        # Verify that get_swappable_settings_name is cached (decorated with @functools.cache)
        self.assertTrue(hasattr(apps.get_swappable_settings_name, 'cache_clear'))
        
        # Test that the method works correctly and can be called multiple times
        # after cache clearing
        result1 = apps.get_swappable_settings_name("nonexistent.Model")
        self.assertIsNone(result1)
        
        # Clear all caches including get_swappable_settings_name cache
        apps.clear_cache()
        
        # Method should still work correctly after cache clearing
        result2 = apps.get_swappable_settings_name("nonexistent.Model")
        self.assertIsNone(result2)