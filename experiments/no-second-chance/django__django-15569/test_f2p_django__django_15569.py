"""
Test for Django bug #15569: RegisterLookupMixin._unregister_lookup() should clear the lookup cache.
"""

from django.db.models import Model, CharField
from django.db.models.query_utils import RegisterLookupMixin
from django.test import TestCase


class TestRegisterLookupMixin(TestCase):
    
    def test_unregister_lookup_clears_cache(self):
        """
        Test that _unregister_lookup method clears the lookup cache.
        
        Before the fix, _unregister_lookup would not call _clear_cached_lookups,
        which would cause cached lookups to remain in the cache even after
        the lookup was unregistered.
        """
        
        # Define a custom lookup class
        class MyLookup(RegisterLookupMixin):
            lookup_name = "my_lookup"
            
            def as_sql(self, compiler, connection):
                return "MY_LOOKUP", []
        
        # Register the lookup
        MyLookup.register_lookup(MyLookup)
        
        # Verify that lookups are available 
        initial_lookups = MyLookup.get_lookups()
        self.assertIn("my_lookup", initial_lookups)
        
        # Unregister the lookup
        MyLookup._unregister_lookup(MyLookup)
        
        # The lookup should no longer be available
        # This would fail if cache is not cleared properly
        lookups_after_unregistration = MyLookup.get_lookups()
        self.assertNotIn("my_lookup", lookups_after_unregistration)

        
    def test_cache_clearing_behavior(self):
        """
        Test that demonstrates the specific problem with cache not being cleared.
        
        This tests the state that would occur when trying to access 
        cached lookups after unregistering them.
        """
        
        # Define a custom lookup class
        class TestLookup(RegisterLookupMixin):
            lookup_name = "test_lookup"
            
            def as_sql(self, compiler, connection):
                return "TEST_LOOKUP", []
        
        # Register the lookup
        TestLookup.register_lookup(TestLookup)
        
        # Force a cache entry by getting lookups once 
        TestLookup.get_lookups()
        
        # Unregister the lookup without clearing cache (old behavior)
        TestLookup._unregister_lookup(TestLookup)
        
        # Now get lookups again - they should not include test_lookup
        # If cache is not cleared, the lookup may still be cached
        lookups = TestLookup.get_lookups()
        self.assertNotIn("test_lookup", lookups)