import unittest
from django.db.models import Field
from django.db.models.lookups import Lookup
from django.test.utils import register_lookup


class TestLookupCacheInvalidation(unittest.TestCase):
    def test_unregister_lookup_clears_cache(self):
        """Test that _unregister_lookup clears the lookup cache."""
        
        # Create a custom lookup class for testing
        class CustomLookup(Lookup):
            lookup_name = 'custom'
            
            def as_sql(self, compiler, connection):
                raise NotImplementedError
                
        # Register a lookup on Field class
        Field.register_lookup(CustomLookup)
        
        # Call get_lookups() to populate the cache (this will cache the result)
        lookups_before = Field.get_lookups()
        
        # Verify the lookup is present
        self.assertIn('custom', lookups_before)
        
        # Unregister the lookup
        Field._unregister_lookup(CustomLookup)
        
        # Call get_lookups() again - this should return fresh results without the unregistered lookup
        lookups_after = Field.get_lookups()
        
        # The unregistered lookup should not be in the results
        # This assertion will fail in the buggy version, but pass in the fixed version
        self.assertNotIn('custom', lookups_after)