import unittest
from django.apps import apps
from django.apps.registry import Apps
from django.test import TestCase


class SwappableSettingsCacheTest(TestCase):
    def test_clear_cache_clears_get_swappable_settings_name_cache(self):
        """
        Test that clear_cache() properly clears the cache of get_swappable_settings_name.
        
        This is a regression test for Django issue #17029.
        The bug was that Apps.clear_cache() did not clear the cache of
        get_swappable_settings_name, which is decorated with @functools.cache.
        """
        # Create a new Apps instance for testing
        test_apps = Apps()
        
        # Call get_swappable_settings_name to populate its cache
        # First call should miss cache
        result1 = test_apps.get_swappable_settings_name("auth.user")
        
        # Check that cache has been populated (currsize > 0)
        cache_info = test_apps.get_swappable_settings_name.cache_info()
        self.assertGreater(cache_info.currsize, 0, 
                         "Cache should be populated after first call")
        
        # Second call should hit cache
        result2 = test_apps.get_swappable_settings_name("auth.user")
        
        # Verify that we got the same result
        self.assertEqual(result1, result2)
        
        # Now clear the cache
        test_apps.clear_cache()
        
        # After clearing cache, cache size should be 0
        cache_info_after = test_apps.get_swappable_settings_name.cache_info()
        self.assertEqual(cache_info_after.currsize, 0,
                        "Cache should be cleared after calling clear_cache()")
        
        # Verify that we can still call the method after cache clear
        result3 = test_apps.get_swappable_settings_name("auth.user")
        self.assertIsNone(result3)  # Should return None for non-swapped models


if __name__ == '__main__':
    unittest.main()