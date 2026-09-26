"""
Regression test for Django issue where named tuples used as arguments to __range
filters cause TypeError in Django 3.0.

This test should fail with the old buggy code and pass with the fixed code.
"""
from collections import namedtuple
from django.test import TestCase
from django.db.models.sql.query import Query


class NamedTupleRangeLookupTest(TestCase):
    """Test for named tuple handling in range lookups."""

    def test_namedtuple_range_lookup(self):
        """Test that named tuples work correctly with __range lookups."""
        # Create a named tuple type
        RangeTuple = namedtuple('RangeTuple', ['start', 'end'])
        
        # Create a mock query object
        query = Query(model=None)
        
        # This should not raise a TypeError
        range_tuple = RangeTuple(1, 10)
        result = query.resolve_lookup_value(range_tuple, can_reuse=[], allow_joins=True)
        
        # The result should be a new named tuple with the same values
        self.assertIsInstance(result, RangeTuple)
        self.assertEqual(result.start, 1)
        self.assertEqual(result.end, 10)

    def test_regular_tuple_range_lookup(self):
        """Test that regular tuples still work correctly."""
        # Create a mock query object
        query = Query(model=None)
        
        # This should work fine
        range_tuple = (1, 10)
        result = query.resolve_lookup_value(range_tuple, can_reuse=[], allow_joins=True)
        
        # The result should be a new tuple with the same values
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 10)