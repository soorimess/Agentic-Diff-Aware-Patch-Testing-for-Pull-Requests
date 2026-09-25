"""
Regression test for Django issue #15569:
RegisterLookupMixin._unregister_lookup() should clear the lookup cache.

This test verifies the specific behavior that when _unregister_lookup() is called,
it properly clears the lookup cache so get_lookups() won't return unregistered lookups.
"""
from django.db.models.query_utils import RegisterLookupMixin
from django.db.models.lookups import Lookup


class TestLookup(Lookup):
    lookup_name = 'test_lookup'


class TestRegisterLookupMixin(RegisterLookupMixin):
    pass


def test_unregister_lookup_clears_cache():
    """
    Test that unregistering a lookup properly clears the lookup cache.
    
    This test fails on the buggy version and would pass after the fix.
    """
    # Register a lookup
    TestRegisterLookupMixin.register_lookup(TestLookup)
    
    # Access get_lookups() to populate the cache (this calls functools.lru_cache)
    lookups_before = TestRegisterLookupMixin.get_lookups()
    
    # Verify lookup is present in cached result
    assert 'test_lookup' in lookups_before
    
    # Now unregister the lookup - this is the key test
    TestRegisterLookupMixin._unregister_lookup(TestLookup)
    
    # Access get_lookups() again - after fix, this should NOT return the unregistered lookup  
    lookups_after = TestRegisterLookupMixin.get_lookups()
    
    # The fix ensures that the unregistered lookup is no longer returned
    assert 'test_lookup' not in lookups_after


def test_unregister_lookup_cache_clearing_behavior():
    """
    Additional verification that cache is properly cleared.
    """
    # Ensure we start clean
    TestRegisterLookupMixin.register_lookup(TestLookup)
    TestRegisterLookupMixin._unregister_lookup(TestLookup)
    
    # Register and access
    TestRegisterLookupMixin.register_lookup(TestLookup)
    lookups_with_cache = TestRegisterLookupMixin.get_lookups()
    assert 'test_lookup' in lookups_with_cache

    # Unregister and verify cache clear
    TestRegisterLookupMixin._unregister_lookup(TestLookup)
    lookups_after_unregistration = TestRegisterLookupMixin.get_lookups() 
    assert 'test_lookup' not in lookups_after_unregistration