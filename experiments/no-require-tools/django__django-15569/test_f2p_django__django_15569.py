"""
Regression test for Django issue #15569:

RegisterLookupMixin._unregister_lookup() should clear the lookup cache.
"""
from django.db.models.fields import Field
from django.db.models.lookups import Lookup
from django.test import TestCase


class DummyLookup(Lookup):
    lookup_name = 'dummy'

    def as_sql(self, compiler, connection):
        raise NotImplementedError()


class TestUnregisterLookupCacheClear(TestCase):
    
    def test_unregister_lookup_caches_correctly_after_fix(self):
        """
        Test for issue 15569: _unregister_lookup should clear lookup cache.
        
        The way we test this is:
        1. Register a lookup 
        2. Call get_lookups() - this caches the result 
        3. Unregister the lookup (the bug: doesn't clear cache)
        4. Call get_lookups() again - should not contain the unregistered lookup
           but may still contain it due to cache
        
        We specifically hit the exact difference between:
        - BEFORE the fix: Old cached result is served
        - AFTER the fix: Fresh lookups result is computed
        """
        # Register a custom lookup
        Field.register_lookup(DummyLookup)
        
        # Access the lookups which will cache result
        lookups1 = Field.get_lookups()
        self.assertIn('dummy', lookups1)
        
        # Unregister the lookup - THIS IS WHERE THE BUG IS
        # Before fix: cache is not cleared, so get_lookups() returns cached result
        # After fix: cache is cleared, so get_lookups() returns fresh result
        Field._unregister_lookup(DummyLookup)
        
        # Now access get_lookups() again 
        # If the fix is applied, demand that dummy is NOT in the result
        # If the bug remains, this assertion would incorrectly pass
        lookups2 = Field.get_lookups()
        
        # The fix ensures that dummy is no longer in lookups, because 
        # _clear_cached_lookups() is called in _unregister_lookup
        self.assertNotIn('dummy', lookups2)
        
    def test_harder_cache_bypassing_pattern(self):
        """
        Test patterns with multiple calls that might manifest the cache bug.
        """
        # Clear cache to make sure we're at a fresh start
        Field.get_lookups.cache_clear()
        
        # Register some lookups
        Field.register_lookup(DummyLookup)
        d1 = getattr(Field, 'class_lookups', {}).get('dummy')
        self.assertIsNotNone(d1)
        
        # Get lookups once (caching happens)  
        lookups1 = Field.get_lookups()
        self.assertIn('dummy', lookups1)
        
        # Unregister the lookup
        Field._unregister_lookup(DummyLookup)
        
        # Now at this point, even new lookups should not have the dummy lookup
        d2 = getattr(Field, 'class_lookups', {}).get('dummy')
        self.assertIsNone(d2)  # class_lookups should not contain 'dummy' anymore
        
        # But there could be caching still happening - let's make another access
        lookups2 = Field.get_lookups()
        self.assertNotIn('dummy', lookups2)