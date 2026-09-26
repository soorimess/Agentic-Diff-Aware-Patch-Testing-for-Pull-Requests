import unittest
from collections import namedtuple
from django.db.models.sql.query import Query
from django.test import TestCase


class RangeFilterWithNamedTupleTest(TestCase):
    def test_range_filter_with_namedtuple(self):
        """
        Test that named tuples can be used as arguments to __range filters.
        This is a regression test for Django issue #13590.
        """
        # Create a mock model for testing
        class TestModel:
            class _meta:
                app_label = 'test'

        # Create a named tuple to use as range argument (like what would be used in a query)
        RangeTuple = namedtuple('RangeTuple', ['start', 'end'])
        range_args = RangeTuple(10, 20)
        
        # This should not raise a TypeError about missing positional arguments
        # The old code would fail here with: 
        # TypeError: __new__() missing 1 required positional argument: 'end'
        try:
            # Create a query object and test the resolve_lookup_value method directly
            query = Query(TestModel)
            
            # This should work without raising TypeError - this is the core of the bug
            result = query.resolve_lookup_value(range_args, can_reuse=[], allow_joins=True)
            
            # The result should be the same type (namedtuple) with resolved values
            self.assertIsInstance(result, RangeTuple)
            self.assertEqual(result.start, 10)
            self.assertEqual(result.end, 20)
            
        except TypeError as e:
            if "missing 1 required positional argument" in str(e):
                self.fail(f"Named tuple range filter failed with: {e}")
            raise

    def test_range_filter_with_regular_tuple(self):
        """
        Test that regular tuples still work (regression test).
        """
        # Create a mock model for testing
        class TestModel:
            class _meta:
                app_label = 'test'

        # Create a regular tuple to use as range argument
        range_args = (10, 20)
        
        # Create a query object and test the resolve_lookup_value method directly
        query = Query(TestModel)
        
        # This should work without raising TypeError
        result = query.resolve_lookup_value(range_args, can_reuse=[], allow_joins=True)
        
        # The result should be the same type (tuple) with resolved values
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0], 10)
        self.assertEqual(result[1], 20)