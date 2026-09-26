import unittest
from collections import namedtuple
from django.test import TestCase


class RangeNamedTupleTest(TestCase):
    """
    Test that named tuples used as arguments to __range work correctly.
    This is a regression test for Django issue #13590.
    """
    
    def test_namedtuple_range_lookup(self):
        """
        Test that named tuples used in range lookups work correctly.
        Before the fix, this would raise TypeError: __new__() missing 1 required positional argument: 'far'
        """
        # Create a named tuple type
        Range = namedtuple('Range', ['near', 'far'])
        
        # Create a range tuple
        range_tuple = Range(near=10, far=20)
        
        # This should work without raising an exception
        # The bug was in resolve_lookup_value when it tried to reconstruct
        # the named tuple with an iterator instead of unpacking it
        from django.db.models.sql.query import Query
        
        # Create a mock query object
        query = Query(None)
        
        # This is the call that was failing in the original code
        result = query.resolve_lookup_value(range_tuple, can_reuse=[], allow_joins=True)
        
        # The result should be the same named tuple type with resolved values
        self.assertIsInstance(result, Range)
        self.assertEqual(result.near, 10)
        self.assertEqual(result.far, 20)

    def test_regular_tuple_range_lookup(self):
        """
        Test that regular tuples still work (regression check).
        """
        # Create a regular tuple
        range_tuple = (10, 20)
        
        from django.db.models.sql.query import Query
        
        # This should work without issues
        query = Query(None)
        result = query.resolve_lookup_value(range_tuple, can_reuse=[], allow_joins=True)
        
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (10, 20))

    def test_list_range_lookup(self):
        """
        Test that lists still work (regression check).
        """
        # Create a list
        range_list = [10, 20]
        
        from django.db.models.sql.query import Query
        
        # This should work without issues
        query = Query(None)
        result = query.resolve_lookup_value(range_list, can_reuse=[], allow_joins=True)
        
        self.assertIsInstance(result, list)
        self.assertEqual(result, [10, 20])