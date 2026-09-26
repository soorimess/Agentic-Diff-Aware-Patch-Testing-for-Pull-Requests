import unittest
from django.db.models import CharField
from django.db.models.query_utils import RegisterLookupMixin
from django.db.models.lookups import Lookup


class TestRegisterLookupMixin(unittest.TestCase):
    def test_unregister_lookup_clears_cache(self):
        """Test that _unregister_lookup clears the lookup cache."""
        
        # Create a custom lookup class for testing
        class CustomLookup(Lookup):
            lookup_name = 'custom'
            
            def as_sql(self, compiler, connection):
                raise NotImplementedError()
        
        # Register a lookup
        RegisterLookupMixin.register_lookup(CustomLookup)
        
        # Get lookups to populate cache
        initial_lookups = RegisterLookupMixin.get_lookups()
        
        # Verify the lookup is registered
        self.assertIn('custom', initial_lookups)
        
        # Unregister the lookup
        RegisterLookupMixin._unregister_lookup(CustomLookup)
        
        # Get lookups again - this should clear the cache and not contain the unregistered lookup
        updated_lookups = RegisterLookupMixin.get_lookups()
        
        # The lookup should no longer be in the lookups
        self.assertNotIn('custom', updated_lookups)
        
        # Test that the cache is properly cleared by calling get_lookups multiple times
        # This tests that subsequent calls don't return stale cached data
        for i in range(3):
            lookups = RegisterLookupMixin.get_lookups()
            self.assertNotIn('custom', lookups)