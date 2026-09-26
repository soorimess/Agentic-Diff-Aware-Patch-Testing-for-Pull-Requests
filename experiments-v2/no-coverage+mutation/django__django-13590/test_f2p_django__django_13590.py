import unittest
from collections import namedtuple
from django.db.models.sql.query import Query


class RangeNamedTupleTest(unittest.TestCase):
    def test_named_tuple_range_lookup(self):
        """Test that named tuples work as arguments to __range lookups."""
        # Create a named tuple similar to what would be used in range queries
        RangeTuple = namedtuple('RangeTuple', ['low', 'high'])
        range_tuple = RangeTuple(low=10, high=20)
        
        # Create a mock query object
        query = Query(model=None)
        
        # This should not raise a TypeError
        # Before the fix, this would fail with:
        # TypeError: __new__() missing 1 required positional argument: 'high'
        result = query.resolve_lookup_value(range_tuple, can_reuse=[], allow_joins=True)
        # The result should be the same type (named tuple) with resolved values
        self.assertIsInstance(result, RangeTuple)
        # The values should be resolved (in this simple case, they should be the same)
        self.assertEqual(result.low, 10)
        self.assertEqual(result.high, 20)

    def test_regular_tuple_still_works(self):
        """Test that regular tuples still work correctly."""
        regular_tuple = (10, 20)
        
        # Create a mock query object
        query = Query(model=None)
        
        result = query.resolve_lookup_value(regular_tuple, can_reuse=[], allow_joins=True)
        # The result should be a regular tuple with resolved values
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (10, 20))

    def test_list_still_works(self):
        """Test that lists still work correctly."""
        regular_list = [10, 20]
        
        # Create a mock query object
        query = Query(model=None)
        
        result = query.resolve_lookup_value(regular_list, can_reuse=[], allow_joins=True)
        # The result should be a list with resolved values
        self.assertIsInstance(result, list)
        self.assertEqual(result, [10, 20])


if __name__ == '__main__':
    unittest.main()