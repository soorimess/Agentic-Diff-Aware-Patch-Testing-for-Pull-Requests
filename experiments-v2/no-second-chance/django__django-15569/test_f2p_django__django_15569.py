import unittest
from django.db import models
from django.test.utils import register_lookup


class TestLookupCacheClearing(unittest.TestCase):
    def test_unregister_lookup_clears_cache(self):
        """Test that _unregister_lookup clears the lookup cache."""
        # Create a custom lookup class
        class TestLookup(models.Lookup):
            lookup_name = "test_lookup"

            def as_sql(self, compiler, connection):
                lhs, params = self.process_lhs(compiler, connection)
                return "%s = %s" % (lhs, self.rhs), params

        # Register the lookup using the direct method (not context manager)
        models.CharField.register_lookup(TestLookup)
        
        # Verify the lookup is registered by checking get_lookups()
        lookups = models.CharField.get_lookups()
        self.assertIn("test_lookup", lookups)
        
        # Now unregister the lookup - this is where the bug manifests
        models.CharField._unregister_lookup(TestLookup)
        
        # The lookup should be removed from class_lookups
        self.assertNotIn("test_lookup", models.CharField.class_lookups)
        
        # The critical test: get_lookups() should not return the unregistered lookup
        # This is the cache clearing bug - if cache isn't cleared, it will still be there
        lookups_after = models.CharField.get_lookups()
        
        # This assertion should pass if the cache is properly cleared
        # But will fail if the bug exists (cache not cleared)
        self.assertNotIn("test_lookup", lookups_after)
        
        # Additional verification: we can also check that the cache was cleared
        # by calling get_lookups() multiple times and ensuring it behaves correctly
        lookups_again = models.CharField.get_lookups()
        self.assertNotIn("test_lookup", lookups_again)
        
        # Test that we can register the same lookup again (should work)
        models.CharField.register_lookup(TestLookup)
        lookups_reregistered = models.CharField.get_lookups()
        self.assertIn("test_lookup", lookups_reregistered)