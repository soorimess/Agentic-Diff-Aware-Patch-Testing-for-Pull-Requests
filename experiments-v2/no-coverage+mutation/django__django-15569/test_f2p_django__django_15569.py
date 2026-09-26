import unittest
from django.db import models


class TestLookupCacheClearing(unittest.TestCase):
    def test_unregister_lookup_clears_cache_as_expected(self):
        """
        Test that verifies _unregister_lookup clears the lookup cache properly.
        
        This test ensures that after unregistering a lookup, subsequent calls to
        get_lookups() do not return the unregistered lookup, demonstrating that
        the cache was properly invalidated.
        """
        
        # Create a custom lookup class
        class TestLookup(models.Lookup):
            lookup_name = "test_lookup"
            
            def as_sql(self, compiler, connection):
                lhs, params = self.process_lhs(compiler, connection)
                return "%s = %s" % (lhs, self.rhs), params
        
        # Register the lookup
        models.CharField.register_lookup(TestLookup)
        
        # Verify it's registered
        lookups_before = models.CharField.get_lookups()
        self.assertIn("test_lookup", lookups_before)
        
        # Clear the cache to ensure we're testing the right behavior
        models.CharField.get_lookups.cache_clear()
        
        # Unregister the lookup - this should clear the cache
        models.CharField._unregister_lookup(TestLookup)
        
        # Verify that the lookup is no longer in get_lookups results
        lookups_after = models.CharField.get_lookups()
        self.assertNotIn("test_lookup", lookups_after)