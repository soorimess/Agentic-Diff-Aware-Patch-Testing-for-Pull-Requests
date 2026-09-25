"""
Test for Django issue #15569.

RegisterLookupMixin._unregister_lookup() should clear the lookup cache.
"""

def test_unregister_lookup_cache():
    """Test demonstrating the cache invalidation bug in _unregister_lookup."""
    # Import inside function to ensure proper test collection
    from django.db.models.query_utils import RegisterLookupMixin
    from django.db.models.lookups import Lookup
    
    class TestLookup(Lookup):
        lookup_name = 'test_lookup'
    
    # Register a lookup
    RegisterLookupMixin.register_lookup(TestLookup)
    
    # Call get_lookups to populate the cache
    lookups1 = RegisterLookupMixin.get_lookups()
    
    # Verify lookup is registered
    assert 'test_lookup' in lookups1, "Lookup should be present after registration"
    
    # Unregister the lookup
    RegisterLookupMixin._unregister_lookup(TestLookup)
    
    # Check if cache was cleared (this is what will fail in buggy version)
    lookups2 = RegisterLookupMixin.get_lookups()
    
    # The assertion that should pass after fix
    assert 'test_lookup' not in lookups2, "Lookup should not be present after unregistration"