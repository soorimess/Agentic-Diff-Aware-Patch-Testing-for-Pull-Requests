"""
Regression tests for Django ticket #15569:
RegisterLookupMixin._unregister_lookup() should clear the lookup cache.
"""
from django.db import models
from django.test import TestCase
from django.test.utils import register_lookup


class CustomLookup(models.Lookup):
    lookup_name = 'custom'

    def as_sql(self, compiler, connection):
        return "custom_sql", []


class TestUnregisterLookupCacheClear(TestCase):
    def test_unregister_lookup_removes_cache_entry(self):
        """
        Test that _unregister_lookup properly removes lookups from the cache.
        
        Before the fix, after unregistering a lookup, the cached lookups 
        in get_lookups() would still include the removed lookup due to 
        not clearing the cache.
        """
        # Register the lookup
        MyField = models.CharField
        MyField.register_lookup(CustomLookup)
        
        # Verify the lookup is registered
        self.assertIn('custom', MyField.class_lookups)
        self.assertIn('custom', MyField.get_lookups())
        
        # Now unregister the lookup  
        MyField._unregister_lookup(CustomLookup)
        
        # The lookup should be gone from both class_lookups AND get_lookups()
        # This is the key test - it should NOT be found in get_lookups()
        # if the cache was properly cleared
        self.assertNotIn('custom', MyField.class_lookups)
        self.assertNotIn('custom', MyField.get_lookups())
        
        # Test that accessing it directly raises KeyError 
        with self.assertRaises(KeyError):
            _ = MyField.class_lookups['custom']