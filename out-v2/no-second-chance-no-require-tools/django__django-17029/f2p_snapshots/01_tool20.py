import unittest
from django.apps import apps
from django.apps.registry import Apps


class SwappableSettingsNameCacheTest(unittest.TestCase):
    def test_clear_cache_calls_get_swappable_settings_name_cache_clear(self):
        """
        Test that Apps.clear_cache() calls cache_clear() on get_swappable_settings_name.
        
        This is a regression test for Django ticket #17029.
        The fix adds self.get_swappable_settings_name.cache_clear() to the clear_cache method.
        """
        # Create a new Apps instance for testing
        test_apps = Apps()
        
        # Verify that get_swappable_settings_name has cache_clear method
        # This should be true for the fixed version
        self.assertTrue(hasattr(test_apps.get_swappable_settings_name, 'cache_clear'))
        
        # Verify that the underlying cached function also has cache_clear
        # This is how functools.cache works
        self.assertTrue(hasattr(test_apps.get_swappable_settings_name.__func__, 'cache_clear'))
        
        # Test the actual fix: create a mock to verify cache_clear is called
        # We'll check that the clear_cache method actually calls cache_clear on the function
        original_cache_clear = test_apps.get_swappable_settings_name.__func__.cache_clear
        
        # Track if cache_clear was called
        cache_clear_called = [False]
        
        def mock_cache_clear():
            cache_clear_called[0] = True
            return original_cache_clear()
            
        # Replace the cache_clear method temporarily
        test_apps.get_swappable_settings_name.__func__.cache_clear = mock_cache_clear
        
        # Call clear_cache - this should trigger our mock
        test_apps.clear_cache()
        
        # Verify that cache_clear was called (this is what the fix does)
        self.assertTrue(cache_clear_called[0], 
                       "clear_cache() should call cache_clear() on get_swappable_settings_name")
        
        # Restore original method
        test_apps.get_swappable_settings_name.__func__.cache_clear = original_cache_clear