import unittest
from django.db.models import CharField
from django.test.utils import register_lookup
from django.db.models.query_utils import RegisterLookupMixin
from django.db.models.lookups import Lookup


class TestRegisterLookupMixin(unittest.TestCase):
    def test_unregister_lookup_clears_cache(self):
        """Test that _unregister_lookup clears the lookup cache."""
        
        # Create a custom lookup class for testing
        class CustomLookup(Lookup):
            lookup_name = "custom"
            
            def as_sql(self, compiler, connection):
                raise NotImplementedError
                
        # Register the lookup
        RegisterLookupMixin.register_lookup(CustomLookup)
        
        # Verify it's registered
        lookups = RegisterLookupMixin.get_lookups()
        self.assertIn("custom", lookups)
        
        # Unregister the lookup
        RegisterLookupMixin._unregister_lookup(CustomLookup)
        
        # After unregistering, the cache should be cleared and the lookup should not be found
        # This is the key test - if cache is not cleared, the old cached result will be returned
        lookups_after = RegisterLookupMixin.get_lookups()
        self.assertNotIn("custom", lookups_after)