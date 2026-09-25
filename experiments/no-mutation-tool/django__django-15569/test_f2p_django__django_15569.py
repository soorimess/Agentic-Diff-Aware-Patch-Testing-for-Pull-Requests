"""
Regression test for Django PR #15569:
RegisterLookupMixin._unregister_lookup() should clear the lookup cache.

This test verifies that after unregistering a lookup, the cached results 
are cleared such that the lookup is not returned in subsequent calls to get_lookups().
"""
from django.test import TestCase
from django.db.models import Field
from django.db.models.lookups import Lookup


class TestRegisterLookupMixin(TestCase):
    def test_unregister_lookup_clears_cache(self):
        """
        Test that _unregister_lookup() clears cached lookups so unregistered 
        lookups are not returned in subsequent get_lookups() calls.
        """
        # Create a custom lookup class 
        class MyLookup(Lookup):
            lookup_name = 'my_lookup'

            def as_sql(self, compiler, connection):
                return 'my_sql', []

        # Register the lookup
        Field.register_lookup(MyLookup)
        
        # Verify the lookup is registered - should appear in get_lookups()
        lookups = Field.get_lookups()
        self.assertIn('my_lookup', lookups)
        
        # Unregister the lookup - this should clear the cache
        Field._unregister_lookup(MyLookup)
        
        # Verify the lookup is no longer available after unregistering
        # This test fails before the fix because the cache is not cleared
        lookups = Field.get_lookups() 
        self.assertNotIn('my_lookup', lookups)