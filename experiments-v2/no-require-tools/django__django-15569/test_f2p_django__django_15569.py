import unittest
from django.db.models import CharField, IntegerField
from django.db.models.query_utils import RegisterLookupMixin
from django.db.models.lookups import Lookup


class TestRegisterLookupMixin(unittest.TestCase):
    def test_unregister_lookup_clears_cache(self):
        """Test that _unregister_lookup clears the lookup cache."""
        # Create a simple lookup class for testing
        class TestLookup(Lookup):
            lookup_name = 'test_lookup'
            
            def as_sql(self, compiler, connection):
                raise NotImplementedError()
        
        # Register the lookup
        RegisterLookupMixin.register_lookup(TestLookup)
        
        # Verify the lookup is registered
        lookups = RegisterLookupMixin.get_lookups()
        self.assertIn('test_lookup', lookups)
        
        # Unregister the lookup
        RegisterLookupMixin._unregister_lookup(TestLookup)
        
        # Verify the lookup is no longer in the cached results
        # This should pass after the fix, but fail before the fix due to caching
        lookups = RegisterLookupMixin.get_lookups()
        self.assertNotIn('test_lookup', lookups)
        
    def test_unregister_lookup_with_custom_name(self):
        """Test that _unregister_lookup clears cache when using custom lookup name."""
        # Create a simple lookup class for testing
        class TestLookup(Lookup):
            lookup_name = 'custom_lookup'
            
            def as_sql(self, compiler, connection):
                raise NotImplementedError()
        
        # Register the lookup with a custom name
        RegisterLookupMixin.register_lookup(TestLookup, 'my_custom_name')
        
        # Verify the lookup is registered
        lookups = RegisterLookupMixin.get_lookups()
        self.assertIn('my_custom_name', lookups)
        
        # Unregister the lookup by name
        RegisterLookupMixin._unregister_lookup(TestLookup, 'my_custom_name')
        
        # Verify the lookup is no longer in the cached results
        lookups = RegisterLookupMixin.get_lookups()
        self.assertNotIn('my_custom_name', lookups)
        
    def test_multiple_lookups_cache_clearing(self):
        """Test that unregistering multiple lookups clears cache properly."""
        # Create simple lookup classes for testing
        class TestLookup1(Lookup):
            lookup_name = 'test_lookup1'
            
            def as_sql(self, compiler, connection):
                raise NotImplementedError()
                
        class TestLookup2(Lookup):
            lookup_name = 'test_lookup2'
            
            def as_sql(self, compiler, connection):
                raise NotImplementedError()
        
        # Register both lookups
        RegisterLookupMixin.register_lookup(TestLookup1)
        RegisterLookupMixin.register_lookup(TestLookup2)
        
        # Verify both lookups are registered
        lookups = RegisterLookupMixin.get_lookups()
        self.assertIn('test_lookup1', lookups)
        self.assertIn('test_lookup2', lookups)
        
        # Unregister one lookup
        RegisterLookupMixin._unregister_lookup(TestLookup1)
        
        # Verify only one is removed from cached results
        lookups = RegisterLookupMixin.get_lookups()
        self.assertNotIn('test_lookup1', lookups)
        self.assertIn('test_lookup2', lookups)
        
        # Unregister the second lookup
        RegisterLookupMixin._unregister_lookup(TestLookup2)
        
        # Verify both are removed from cached results
        lookups = RegisterLookupMixin.get_lookups()
        self.assertNotIn('test_lookup1', lookups)
        self.assertNotIn('test_lookup2', lookups)