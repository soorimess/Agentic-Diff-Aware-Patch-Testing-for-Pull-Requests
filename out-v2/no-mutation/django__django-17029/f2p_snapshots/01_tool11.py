import unittest
from django.apps import apps
from django.apps.registry import Apps


class SwappableSettingsCacheTest(unittest.TestCase):
    def test_clear_cache_clears_swappable_settings_name_cache(self):
        """
        Test that Apps.clear_cache() clears the get_swappable_settings_name cache.
        
        Before the fix, calling clear_cache() would not clear the LRU cache
        for get_swappable_settings_name, causing it to return cached values
        even after the app registry had been reset.
        """
        # Create a new Apps instance to test with
        test_apps = Apps()
        
        # Call get_swappable_settings_name to populate the cache
        result1 = test_apps.get_swappable_settings_name("auth.User")
        
        # Verify that the cache has been populated by checking cache info
        cache_info_before = test_apps.get_swappable_settings_name.cache_info()
        # Should have at least one miss and possibly some hits
        self.assertGreaterEqual(cache_info_before.misses, 0)
        
        # Call it again to make sure cache has some hits
        result2 = test_apps.get_swappable_settings_name("auth.User")
        cache_info_after_first_call = test_apps.get_swappable_settings_name.cache_info()
        
        # Now clear the cache
        test_apps.clear_cache()
        
        # After clearing, cache should be empty (no hits, no misses, size 0)
        cache_info_after_clear = test_apps.get_swappable_settings_name.cache_info()
        
        # The key assertion: after clear_cache(), the cache should be empty
        # This means misses should be 0 (no cache hits) and currsize should be 0
        self.assertEqual(cache_info_after_clear.currsize, 0, 
                        "Cache size should be 0 after clear_cache()")
        self.assertEqual(cache_info_after_clear.hits, 0,
                        "Cache hits should be 0 after clear_cache()")
        self.assertEqual(cache_info_after_clear.misses, 0,
                        "Cache misses should be 0 after clear_cache()")
        
        # Call again to make sure it's really cleared
        result3 = test_apps.get_swappable_settings_name("auth.User")
        cache_info_final = test_apps.get_swappable_settings_name.cache_info()
        
        # Should now have 1 miss (since it's a fresh cache)
        self.assertEqual(cache_info_final.misses, 1,
                        "Should have 1 miss after cache was cleared and function called again")
        self.assertEqual(cache_info_final.currsize, 1,
                        "Cache should have 1 item after first call post-clear")