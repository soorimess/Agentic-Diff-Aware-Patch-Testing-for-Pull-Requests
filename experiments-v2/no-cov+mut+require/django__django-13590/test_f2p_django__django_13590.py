from collections import namedtuple
from django.test import TestCase


class TestNamedTupleRange(TestCase):
    """Test that named tuples work correctly with __range lookups."""
    
    def test_named_tuple_range_lookup(self):
        """Test that named tuples used as range arguments work correctly."""
        # Create a named tuple type
        RangeTuple = namedtuple('RangeTuple', ['near', 'far'])
        
        # Test with a named tuple - this should not raise TypeError
        # The bug was that resolve_lookup_value would try to reconstruct
        # the named tuple with an iterator, which fails for named tuples
        range_args = RangeTuple(near=10, far=20)
        
        # Create a dummy model class for the query
        class DummyModel:
            class _meta:
                app_label = 'test'
        
        # This should work without raising TypeError: __new__() missing 1 required positional argument: 'far'
        try:
            from django.db.models.sql.query import Query
            query = Query(DummyModel)
            
            # This call should not raise an exception
            result = query.resolve_lookup_value(range_args, can_reuse=[], allow_joins=True)
            
            # Verify that the result is the same type and values
            self.assertIsInstance(result, RangeTuple)
            self.assertEqual(result.near, 10)
            self.assertEqual(result.far, 20)
            
        except TypeError as e:
            if "__new__() missing 1 required positional argument: 'far'" in str(e):
                self.fail("Named tuple range lookup failed with TypeError - this is the bug we're testing for")
            raise