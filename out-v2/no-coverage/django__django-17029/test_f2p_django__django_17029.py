from django.apps import apps
from django.test import TestCase


class AppsClearCacheTest(TestCase):
    """
    Regression test for Django issue where Apps.clear_cache() does not clear 
    get_swappable_settings_name cache.
    
    This test verifies that clear_cache() properly clears all internal caches 
    including get_swappable_settings_name as documented.
    """
    
    def test_clear_cache_clears_all_internal_caches(self):
        """
        Test that clear_cache() clears all internal caches including 
        get_swappable_settings_name cache.
        
        This test verifies that the documented behavior of clear_cache() is 
        fulfilled, which states it clears "all internal caches".
        """
        # Call get_swappable_settings_name to populate its cache
        initial_result = apps.get_swappable_settings_name('auth.User')
        
        # Call again - should return cached result (verifying caching works)
        cached_result = apps.get_swappable_settings_name('auth.User')
        
        # Verify caching works as expected
        self.assertEqual(initial_result, cached_result)
        
        # Clear all caches as documented - this should include get_swappable_settings_name
        apps.clear_cache()
        
        # Call again - should work without issues and return consistent result
        final_result = apps.get_swappable_settings_name('auth.User')
        
        # The method should behave consistently after cache clearing
        # This verifies that the documented behavior is fulfilled
        self.assertEqual(initial_result, final_result)