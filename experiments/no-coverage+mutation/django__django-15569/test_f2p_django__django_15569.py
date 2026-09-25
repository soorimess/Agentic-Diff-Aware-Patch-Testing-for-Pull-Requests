"""
Regression test for Django PR #15569: RegisterLookupMixin._unregister_lookup() 
should clear the lookup cache.
"""
from django.test import TestCase


class RegisterLookupCacheTest(TestCase):
    def test_unregister_lookup_clears_cache(self):
        """
        Test that unregistering a lookup clears the cached lookups.
        
        Before the fix: _unregister_lookup does not clear the lookup cache,
        so get_lookups() continues to return cached results including
        the unregistered lookup.
        
        After the fix: _unregister_lookup calls _clear_cached_lookups(), 
        so subsequent get_lookups() calls return the correct result.
        """
        from django.db.models.lookups import Lookup
        from django.db.models.query_utils import RegisterLookupMixin

        class TestLookup(Lookup):
            lookup_name = 'test_lookup'

        class TestClass(RegisterLookupMixin):
            pass

        # Register a lookup
        TestClass.register_lookup(TestLookup)
        
        # Get lookups to populate cache
        lookups_before = TestClass.get_lookups()
        
        # Verify lookup is registered
        self.assertIn('test_lookup', lookups_before)
        
        # Unregister the lookup (this should clear the cache)
        TestClass._unregister_lookup(TestLookup)
        
        # Get lookups again - should not contain the unregistered lookup
        # This will fail before the fix because cache is not cleared
        lookups_after = TestClass.get_lookups()
        
        # The unregistered lookup should no longer be in the lookups
        self.assertNotIn('test_lookup', lookups_after)

    def test_register_then_unregister_lookup_cache_behavior(self):
        """
        Additional test to verify the cache behavior clearly.
        """
        from django.db.models.lookups import Lookup
        from django.db.models.query_utils import RegisterLookupMixin

        class TestLookup(Lookup):
            lookup_name = 'test_lookup2'

        class TestClass(RegisterLookupMixin):
            pass

        # Clear any existing state
        if hasattr(TestClass, 'class_lookups'):
            TestClass.class_lookups.clear()
        
        # Register a lookup
        TestClass.register_lookup(TestLookup)
        lookups_before = TestClass.get_lookups()
        
        # Verify it's there
        self.assertIn('test_lookup2', lookups_before)
        
        # Unregister it
        TestClass._unregister_lookup(TestLookup)
        
        # Get lookups again - should be cleaned up
        lookups_after = TestClass.get_lookups()
        
        # The test_lookup should not be in the results anymore
        self.assertNotIn('test_lookup2', lookups_after)