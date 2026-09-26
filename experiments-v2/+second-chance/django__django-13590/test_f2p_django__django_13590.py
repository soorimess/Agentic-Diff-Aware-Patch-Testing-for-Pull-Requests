import unittest
from collections import namedtuple
from django.db.models.sql.query import Query


class RangeLookupWithNamedTupleTest(unittest.TestCase):
    """
    Test that named tuples used as arguments to __range work correctly.
    
    This is a regression test for Django issue where named tuples used
    as arguments to __range queryset filters would cause a TypeError
    in resolve_lookup_value method.
    """
    
    def test_named_tuple_range_lookup(self):
        """Test that named tuples work with __range lookups."""
        # Create a named tuple type
        Range = namedtuple('Range', ['start', 'end'])
        
        # Create a mock query object
        query = Query(model=None)
        
        # Create a named tuple instance
        range_tuple = Range(10, 20)
        
        # This should not raise TypeError: __new__() missing 1 required positional argument: 'far'
        try:
            result = query.resolve_lookup_value(range_tuple, can_reuse=[], allow_joins=True)
            # The result should be a new named tuple with the same values
            self.assertIsInstance(result, Range)
            self.assertEqual(result.start, 10)
            self.assertEqual(result.end, 20)
        except TypeError as e:
            if "__new__() missing 1 required positional argument" in str(e):
                self.fail(f"Named tuple range lookup failed with: {e}")
            raise

    def test_regular_tuple_range_lookup(self):
        """Test that regular tuples still work (regression check)."""
        # Create a regular tuple
        range_tuple = (10, 20)
        
        # Create a mock query object
        query = Query(model=None)
        
        # This should work fine
        result = query.resolve_lookup_value(range_tuple, can_reuse=[], allow_joins=True)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (10, 20))

    def test_list_range_lookup(self):
        """Test that lists still work (regression check)."""
        # Create a list
        range_list = [10, 20]
        
        # Create a mock query object
        query = Query(model=None)
        
        # This should work fine
        result = query.resolve_lookup_value(range_list, can_reuse=[], allow_joins=True)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [10, 20])