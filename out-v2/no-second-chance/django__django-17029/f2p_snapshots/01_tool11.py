import unittest
from django.apps import apps
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
        
        # Check initial cache state
        initial_cache_info = test_apps.get_swappable_settings_name.cache_info()
        print(f"Initial cache info: {initial_cache_info}")
        
        # Call get_swappable_settings_name to populate the cache
        # This should cache the result
        result1 = test_apps.get_swappable_settings_name("auth.User")
        print(f"First call result: {result1}")
        
        # Check cache info after first call
        cache_info_after_first = test_apps.get_swappable_settings_name.cache_info()
        print(f"Cache info after first call: {cache_info_after_first}")
        
        # Call it again - this should hit the cache
        result2 = test_apps.get_swappable_settings_name("auth.User")
        print(f"Second call result: {result2}")
        
        cache_info_after_second = test_apps.get_swappable_settings_name.cache_info()
        print(f"Cache info after second call: {cache_info_after_second}")
        
        # The cache should have been hit (hits increased)
        self.assertEqual(cache_info_after_second.hits, cache_info_after_first.hits + 1)
        self.assertEqual(cache_info_after_second.misses, cache_info_after_first.misses)
        
        # Now clear the cache
        test_apps.clear_cache()
        print("Cache cleared")
        
        # After clearing, cache should be reset
        cache_info_after_clear = test_apps.get_swappable_settings_name.cache_info()
        print(f"Cache info after clear: {cache_info_after_clear}")
        
        # Check that cache was actually cleared by calling again
        result3 = test_apps.get_swappable_settings_name("auth.User")
        print(f"Third call result: {result3}")
        cache_info_after_third = test_apps.get_swappable_settings_name.cache_info()
        print(f"Cache info after third call: {cache_info_after_third}")
        
        # The third call should result in a cache miss (misses increased)
        # This assertion should pass if cache is properly cleared
        self.assertEqual(cache_info_after_third.misses, cache_info_after_clear.misses + 1)
        self.assertEqual(cache_info_after_third.hits, cache_info_after_clear.hits)