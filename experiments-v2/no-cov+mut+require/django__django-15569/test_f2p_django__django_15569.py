import unittest
from django.db import models
from django.test import TestCase
from django.test.utils import register_lookup
from django.db.models.query_utils import RegisterLookupMixin


class TestUnregisterLookupCacheClear(TestCase):
    def test_unregister_lookup_clears_cache(self):
        """
        Test that _unregister_lookup clears the lookup cache.
        
        This is a regression test for Django PR #15569.
        Before the fix, _unregister_lookup would not clear the lookup cache,
        causing stale cached lookups to remain accessible even after unregistering.
        """
        # Create a custom lookup class
        class TestLookup(models.Lookup):
            lookup_name = "test_lookup"

            def as_sql(self, compiler, connection):
                return "test_lookup", []

        # Register the lookup directly on RegisterLookupMixin
        RegisterLookupMixin.register_lookup(TestLookup)
        
        # Access the lookups to trigger caching
        lookups = RegisterLookupMixin.get_lookups()
        self.assertIn("test_lookup", lookups)
        
        # Now unregister the lookup
        RegisterLookupMixin._unregister_lookup(TestLookup)
        
        # The lookup should no longer be in the cached lookups
        # Access lookups again to trigger cache rebuild
        lookups_after = RegisterLookupMixin.get_lookups()
        self.assertNotIn("test_lookup", lookups_after)