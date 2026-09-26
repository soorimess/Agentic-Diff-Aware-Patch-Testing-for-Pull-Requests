import unittest
from django.db.models import IntegerField
from django.db.models.query_utils import RegisterLookupMixin


class TestRegisterLookupMixin(unittest.TestCase):
    def test_unregister_lookup_clears_cache(self):
        """Test that _unregister_lookup clears the lookup cache."""
        # Create a custom lookup class
        class TestLookup(IntegerField):
            lookup_name = "test_lookup"
            
            def as_sql(self, compiler, connection):
                return "test_lookup", []
        
        # Manually register the lookup by adding to class_lookups
        if not hasattr(IntegerField, 'class_lookups'):
            IntegerField.class_lookups = {}
        IntegerField.class_lookups["test_lookup"] = TestLookup
        
        # Call get_lookups once to populate the cache
        lookups1 = IntegerField.get_lookups()
        self.assertIn("test_lookup", lookups1)
        
        # Now unregister the lookup
        IntegerField._unregister_lookup(TestLookup)
        
        # Call get_lookups again - should not contain test_lookup anymore
        # The cache should have been cleared by _clear_cached_lookups
        lookups2 = IntegerField.get_lookups()
        self.assertNotIn("test_lookup", lookups2)