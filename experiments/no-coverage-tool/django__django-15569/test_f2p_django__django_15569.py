"""
Regression test for Django issue #15569

The _unregister_lookup() method should clear the lookup cache.
"""
from django.db.models import CharField
from django.db.models.lookups import Lookup
from django.test import TestCase
from django.db.models.query_utils import RegisterLookupMixin


class TestRegisterLookupMixin(TestCase):
    
    def test_unregister_lookup_clears_cache(self):
        """
        Test that _unregister_lookup() clears the lookup cache.
        
        Before the fix: Unregistering a lookup would not clear the cache,
        so get_lookups() would still return the removed lookup.
        
        After the fix: Unregistering a lookup clears the cache,
        so get_lookups() will not return the removed lookup.
        """
        # Add a custom lookup to test with
        class CustomLookup(Lookup):
            lookup_name = 'custom'
            
            def as_sql(self, compiler, connection):
                pass
        
        # Register the lookup
        RegisterLookupMixin.register_lookup(CustomLookup)
        
        # Verify it's in the lookups
        lookups_before = RegisterLookupMixin.get_lookups()
        self.assertIn('custom', lookups_before)
        
        # Unregister the lookup
        RegisterLookupMixin._unregister_lookup(CustomLookup)
        
        # The cache should now be cleared and the lookup should not appear in get_lookups()
        # This is the behavior that should be tested - the cache consistency issue
        lookups_after = RegisterLookupMixin.get_lookups()
        self.assertNotIn('custom', lookups_after)
        
    def test_unregister_lookup_multiple_cycles(self):
        """
        Test that multiple registration/unregistration cycles work correctly
        with cache consistency.
        """
        class TestLookup1(Lookup):
            lookup_name = 'test1'
            
            def as_sql(self, compiler, connection):
                pass

        class TestLookup2(Lookup):
            lookup_name = 'test2'
            
            def as_sql(self, compiler, connection):
                pass

        # Register first lookup
        RegisterLookupMixin.register_lookup(TestLookup1) 
        lookups_1 = RegisterLookupMixin.get_lookups()
        self.assertIn('test1', lookups_1)
        
        # Register second lookup  
        RegisterLookupMixin.register_lookup(TestLookup2)
        lookups_2 = RegisterLookupMixin.get_lookups()
        self.assertIn('test1', lookups_2)
        self.assertIn('test2', lookups_2)
        
        # Unregister first lookup
        RegisterLookupMixin._unregister_lookup(TestLookup1)
        lookups_3 = RegisterLookupMixin.get_lookups()
        self.assertNotIn('test1', lookups_3)
        self.assertIn('test2', lookups_3)
        
        # Unregister second lookup
        RegisterLookupMixin._unregister_lookup(TestLookup2)
        lookups_4 = RegisterLookupMixin.get_lookups()
        self.assertNotIn('test1', lookups_4)
        self.assertNotIn('test2', lookups_4)
        
    def test_different_lookup_names(self):
        """
        Test unregistering with explicit lookup_name parameter.
        """
        class CustomLookup(Lookup):
            lookup_name = 'custom_lookup'
            
            def as_sql(self, compiler, connection):
                pass
        
        # Register the lookup
        RegisterLookupMixin.register_lookup(CustomLookup)
        lookups_before = RegisterLookupMixin.get_lookups()
        self.assertIn('custom_lookup', lookups_before)
        
        # Unregister the lookup using explicit lookup_name
        RegisterLookupMixin._unregister_lookup(CustomLookup, lookup_name='custom_lookup')
        lookups_after = RegisterLookupMixin.get_lookups()
        self.assertNotIn('custom_lookup', lookups_after)