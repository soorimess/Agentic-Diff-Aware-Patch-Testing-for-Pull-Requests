import unittest
from django.apps.registry import Apps


class SwappableSettingsNameCacheTest(unittest.TestCase):
    """
    Test that Apps.clear_cache() clears the get_swappable_settings_name cache.
    """
    
    def test_clear_cache_clears_get_swappable_settings_name_cache(self):
        """
        Regression test for Django issue where Apps.clear_cache() does not clear
        get_swappable_settings_name cache.
        """
        # Create a new Apps instance for testing
        test_apps = Apps()
        
        # Call get_swappable_settings_name to populate the cache
        result1 = test_apps.get_swappable_settings_name("auth.User")
        
        # Verify cache has an entry (should be cached now)
        cache_info_before = test_apps.get_swappable_settings_name.cache_info()
        self.assertEqual(cache_info_before.currsize, 1)
        
        # Call again - should hit cache
        result2 = test_apps.get_swappable_settings_name("auth.User")
        cache_info_after = test_apps.get_swappable_settings_name.cache_info()
        self.assertEqual(cache_info_after.hits, cache_info_before.hits + 1)
        
        # Clear the cache
        test_apps.clear_cache()
        
        # Verify cache is now empty
        cache_info_after_clear = test_apps.get_swappable_settings_name.cache_info()
        self.assertEqual(cache_info_after_clear.currsize, 0)
        self.assertEqual(cache_info_after_clear.hits, 0)
        self.assertEqual(cache_info_after_clear.misses, 0)
        
        # Call again - should miss cache
        result3 = test_apps.get_swappable_settings_name("auth.User")
        cache_info_after_second_call = test_apps.get_swappable_settings_name.cache_info()
        self.assertEqual(cache_info_after_second_call.misses, 1)
        self.assertEqual(cache_info_after_second_call.currsize, 1)