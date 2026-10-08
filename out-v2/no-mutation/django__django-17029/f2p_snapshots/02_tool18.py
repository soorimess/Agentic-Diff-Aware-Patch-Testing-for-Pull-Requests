import unittest
from django.apps.registry import Apps


class SwappableSettingsCacheTest(unittest.TestCase):
    def test_clear_cache_clears_swappable_settings_name_cache(self):
        """
        Test that Apps.clear_cache() clears the get_swappable_settings_name cache.
        
        This test verifies the fix for the bug where Apps.clear_cache() did not
        clear the get_swappable_settings_name cache, which is a functools.lru_cache
        decorated method. The cache should be cleared to ensure that after
        clearing the app registry cache, subsequent calls to get_swappable_settings_name
        don't return stale cached values.
        """
        # Create a new Apps instance to test with
        test_apps = Apps()
        
        # Call get_swappable_settings_name to populate the cache
        result1 = test_apps.get_swappable_settings_name("auth.User")
        
        # Verify that the cache has been populated
        cache_info_before = test_apps.get_swappable_settings_name.cache_info()
        self.assertGreaterEqual(cache_info_before.currsize, 0)
        
        # Call it again to ensure there are cache hits
        result2 = test_apps.get_swappable_settings_name("auth.User")
        cache_info_after_first_call = test_apps.get_swappable_settings_name.cache_info()
        
        # Verify cache has entries
        self.assertEqual(cache_info_after_first_call.currsize, 1)
        
        # Clear the cache - this should clear the get_swappable_settings_name cache too
        test_apps.clear_cache()
        
        # After clearing, the get_swappable_settings_name cache should be empty
        cache_info_after_clear = test_apps.get_swappable_settings_name.cache_info()
        
        # The fix ensures that cache_clear() is called on get_swappable_settings_name
        self.assertEqual(cache_info_after_clear.currsize, 0,
                        "get_swappable_settings_name cache should be cleared by clear_cache()")
        self.assertEqual(cache_info_after_clear.hits, 0,
                        "get_swappable_settings_name cache hits should be reset")
        self.assertEqual(cache_info_after_clear.misses, 0,
                        "get_swappable_settings_name cache misses should be reset")
        
        # Call again to make sure it's really cleared and working properly
        result3 = test_apps.get_swappable_settings_name("auth.User")
        cache_info_final = test_apps.get_swappable_settings_name.cache_info()
        
        # Should now have 1 miss (since it's a fresh cache)  
        self.assertEqual(cache_info_final.misses, 1,
                        "Should have 1 miss after cache was cleared and function called again")
        self.assertEqual(cache_info_final.currsize, 1,
                        "Cache should have 1 item after first call post-clear")