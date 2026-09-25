from django.db.models import CharField
from django.db.models.lookups import Lookup
from django.test import SimpleTestCase
from django.test.utils import register_lookup
from django.db.models.query_utils import RegisterLookupMixin


class CustomLookup(Lookup):
    lookup_name = "custom"


class RegisterLookupCacheTest(SimpleTestCase):
    """
    Test that _unregister_lookup clears the lookup cache.
    
    This test verifies the behavior described in Django PR #15569:
    RegisterLookupMixin._unregister_lookup() should clear the lookup cache.
    """
    
    def test_unregister_lookup_clears_cache(self):
        """
        Test that when a lookup is unregistered, the cache is properly cleared
        so subsequent attempts to get the lookup return None instead of the cached version.
        """
        # Set up the model field
        field = CharField()
        
        # Register a custom lookup
        register_lookup(CharField, CustomLookup)
        
        # Access the lookup to populate the cache - this triggers get_lookups() cache
        lookup = field.get_lookup("custom")
        self.assertIsNotNone(lookup)
        
        # Unregister the lookup
        RegisterLookupMixin._unregister_lookup(CharField, CustomLookup)
        
        # Access the lookup again - should return None now since it's unregistered
        # In the buggy version, this would still return the cached lookup
        lookup_after_unregistration = field.get_lookup("custom")
        
        # This assertion checks that the bug is present - in the buggy version,
        # the lookup would still be found due to cache not being cleared
        self.assertIsNone(lookup_after_unregistration)

    def test_get_lookups_cache_clears_after_unregister(self):
        """
        Test that get_lookups() cache is cleared upon unregistering a lookup.
        """
        # Register a custom lookup
        register_lookup(CharField, CustomLookup)
        
        # Access get_lookups to populate cache
        lookups_before = CharField.get_lookups()
        self.assertIn("custom", lookups_before)
        
        # Unregister the lookup
        RegisterLookupMixin._unregister_lookup(CharField, CustomLookup)
        
        # Check that get_lookups() no longer includes the unregistered lookup
        # In the buggy version, it would still show the cached version
        lookups_after = CharField.get_lookups()
        self.assertNotIn("custom", lookups_after)