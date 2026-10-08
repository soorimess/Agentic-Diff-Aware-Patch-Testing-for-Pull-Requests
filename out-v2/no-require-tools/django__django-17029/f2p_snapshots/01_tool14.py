import unittest
from django.apps import apps
from django.apps.registry import Apps


class SwappableSettingsNameCacheTest(unittest.TestCase):
    """
    Test that Apps.clear_cache() clears the get_swappable_settings_name cache.
    
    This is a regression test for Django issue #17029.
    The bug was that clear_cache() did not clear the cache of
    get_swappable_settings_name, which is decorated with @functools.cache.
    """
    
    def test_clear_cache_clears_swappable_settings_name_cache(self):
        """
        Test that calling clear_cache() invalidates the get_swappable_settings_name cache.
        """
        # Create a fresh Apps instance to test the behavior more directly
        test_apps = Apps()
        
        # Call the method multiple times to populate cache
        result1 = test_apps.get_swappable_settings_name("auth.User")
        result2 = test_apps.get_swappable_settings_name("auth.User")
        result3 = test_apps.get_swappable_settings_name("auth.User")
        
        # Check cache stats - should have 1 miss and 2 hits
        cache_info = test_apps.get_swappable_settings_name.cache_info()
        self.assertEqual(cache_info.hits, 2)  # Two hits after first call
        self.assertEqual(cache_info.misses, 1)  # One miss for first call
        self.assertEqual(cache_info.currsize, 1)  # One item cached
        
        # Clear cache
        test_apps.clear_cache()
        
        # Check cache stats after clear - should be reset
        cache_info_after = test_apps.get_swappable_settings_name.cache_info()
        
        # The cache should be cleared (hits, misses, and currsize should all be 0)
        self.assertEqual(cache_info_after.hits, 0)
        self.assertEqual(cache_info_after.misses, 0)
        self.assertEqual(cache_info_after.currsize, 0)
        
        # Call again to make sure it works after clearing
        result4 = test_apps.get_swappable_settings_name("auth.User")
        cache_info_final = test_apps.get_swappable_settings_name.cache_info()
        
        # Should have 1 miss (first call after clear) and 0 hits
        self.assertEqual(cache_info_final.hits, 0)
        self.assertEqual(cache_info_final.misses, 1)
        self.assertEqual(cache_info_final.currsize, 1)