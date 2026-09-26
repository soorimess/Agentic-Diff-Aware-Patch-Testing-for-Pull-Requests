from django.db.models import CharField
from django.db.models.lookups import Lookup
from django.test import SimpleTestCase


class TestLookupCacheClearing(SimpleTestCase):
    def test_unregister_lookup_clears_cache(self):
        """
        Test that _unregister_lookup() clears the lookup cache.
        
        Before the fix, unregistering a lookup would not clear the cache,
        so subsequent calls to get_lookups() would still return the old cached
        version instead of reflecting the updated state.
        """
        # Create a custom lookup class
        class TestLookup(Lookup):
            lookup_name = "test_lookup"
            
            def as_sql(self, compiler, connection):
                return "test_lookup", []
        
        # Register the lookup manually
        CharField.register_lookup(TestLookup)
        
        # Get lookups to populate the cache
        char_field_lookups = CharField.get_lookups()
        
        # Verify the lookup is registered
        self.assertIn("test_lookup", char_field_lookups)
        
        # Now unregister the lookup
        # This should clear the cache but currently doesn't in the buggy version
        CharField._unregister_lookup(TestLookup)
        
        # Get lookups again - should not contain our unregistered lookup
        char_field_lookups_after = CharField.get_lookups()
        
        # The test should fail on the old code because the cache wasn't cleared
        self.assertNotIn("test_lookup", char_field_lookups_after)