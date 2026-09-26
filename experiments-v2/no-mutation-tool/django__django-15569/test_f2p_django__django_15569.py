import unittest
from django.db.models import Field, CharField
from django.test.utils import register_lookup


class TestLookupCacheClearing(unittest.TestCase):
    def test_unregister_lookup_clears_cache(self):
        """Test that unregister_lookup clears the lookup cache."""
        
        # Create a custom lookup class
        class TestLookup(Field):
            lookup_name = "test_lookup"
            
            def as_sql(self, compiler, connection):
                return "test_lookup", []
        
        # Register the lookup
        with register_lookup(CharField, TestLookup):
            # Verify the lookup is registered by checking get_lookups
            lookups = CharField.get_lookups()
            self.assertIn("test_lookup", lookups)
            
            # The lookup should be accessible through _get_lookup
            lookup = CharField._get_lookup("test_lookup")
            self.assertIsNotNone(lookup)
            
        # After exiting the context manager, the lookup should be unregistered
        # But due to the bug, the cache might still contain the old data
        lookups = CharField.get_lookups()
        self.assertNotIn("test_lookup", lookups)
        
        # The lookup should no longer be accessible
        lookup = CharField._get_lookup("test_lookup")
        self.assertIsNone(lookup)