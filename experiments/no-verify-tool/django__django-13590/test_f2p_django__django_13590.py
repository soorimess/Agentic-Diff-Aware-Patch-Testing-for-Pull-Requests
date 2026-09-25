"""
Test for Django issue with named tuples in range filters.
This directly tests the resolve_lookup_value method that was buggy.
"""
from collections import namedtuple
from django.test import SimpleTestCase


class TestNamedTupleRangeFilter(SimpleTestCase):
    def test_namedtuple_resolution_preserves_type_and_values(self):
        """
        Named tuples should be handled correctly in resolve_lookup_value.
        Before the fix this would raise TypeError: __new__() missing 1 required positional argument.
        """
        from django.db.models.sql.query import Query
        
        # Create a mock model - minimal implementation
        class Model:
            class _meta:
                app_label = 'test'
        
        # Create named tuple as described in bug report
        RangeTuple = namedtuple('RangeTuple', ['start', 'end'])
        value = RangeTuple(10, 20)
        
        # Create Query object 
        query = Query(Model)
        
        # This call should work without TypeError after fix
        result = query.resolve_lookup_value(value, can_reuse=[], allow_joins=True)
        
        # Verify type and value preservation
        self.assertIsInstance(result, RangeTuple)
        self.assertEqual(result.start, 10)
        self.assertEqual(result.end, 20)

    def test_regular_tuple_behavior_unchanged(self):
        """
        Regular tuple behavior should remain unchanged as regression test.
        """
        from django.db.models.sql.query import Query
        
        class Model:
            class _meta:
                app_label = 'test'
        
        # Regular tuple
        value = (10, 20)
        
        query = Query(Model)
        result = query.resolve_lookup_value(value, can_reuse=[], allow_joins=True)
        
        # Should preserve regular tuple type
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (10, 20))