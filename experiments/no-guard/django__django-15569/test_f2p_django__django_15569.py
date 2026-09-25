"""
Regression tests for Django issue #15569.

RegisterLookupMixin._unregister_lookup() should clear the lookup cache.
"""
from django.db.models import CharField
from django.test import TestCase
from django.test.utils import register_lookup


class CustomLookup:
    """A custom lookup for testing"""
    lookup_name = 'custom'

    def as_sql(self, compiler, connection):
        return 'custom_lookup_sql', []


class RegisterLookupMixinCacheTest(TestCase):
    def test_unregister_lookup_clears_cache(self):
        """
        Test that _unregister_lookup clears the lookup cache.
        
        The bug: after unregistering a lookup, cached lookups from 
        get_lookups() are not cleared, so subsequent calls to get_lookups()
        return stale results.
        """
        # Ensure custom lookup is not present
        initial_lookups = CharField.get_lookups()
        self.assertNotIn('custom', initial_lookups)
        
        # Register a custom lookup
        with register_lookup(CharField, CustomLookup):
            # This call establishes the cached result for get_lookups()
            lookups_with_custom = CharField.get_lookups() 
            self.assertIn('custom', lookups_with_custom)
            # Cache is populated, same object every time (this is the LRU cache behavior)
            
        # After the context manager, the lookup should be unregistered
        # The unregistration should clear cached lookups - this is the test
        lookups_after_unregister = CharField.get_lookups()
        
        # This assertion will fail before the fix and pass after the fix
        self.assertNotIn('custom', lookups_after_unregister)
        
        # Verify that we can register it again and it works
        with register_lookup(CharField, CustomLookup):
            lookups_with_custom_again = CharField.get_lookups()
            self.assertIn('custom', lookups_with_custom_again)
            
        # And after second unregistration it should again not be found
        lookups_after_second_unreg = CharField.get_lookups()
        self.assertNotIn('custom', lookups_after_second_unreg)