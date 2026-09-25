"""
Regression test for Django issue where named tuples used as arguments 
to __range filters error when upgrading from 2.2 to 3.0.

The problem occurs in django.db.models.sql.query.Query.resolve_lookup_value when:
1. A named tuple is passed as argument to a range lookup 
2. The method tries to resolve the tuple elements and then reconstruct the tuple
3. Old code: type(value)(<generator>) - passes iterator to namedtuple constructor
4. New code: type_(*values) - properly unpacks the values for namedtuple

This test ensures the behavior change is properly pinned down.
"""
from collections import namedtuple
from django.test import TestCase


class DjangoNamedTupleRangeTest(TestCase):
    def test_namedtuple_range_lookup_bug(self):
        """
        Direct test of the bug described in the issue:
        Named tuples passed to __range filters cause TypeError in Django 3.0+
        """
        # Create a named tuple like what would be used in __range filters
        Point = namedtuple('Point', ['x', 'y'])
        point = Point(1, 2)
        
        # This is the method that was failing in the bug report
        from django.db.models.sql.query import Query
        query = Query(None)
        
        # This should work - the fix allows namedtuples to work properly  
        # Before the fix: TypeError: __new__() missing 1 required positional argument: 'far'
        # After the fix: should return the same namedtuple unchanged 
        result = query.resolve_lookup_value(point, can_reuse=[], allow_joins=True)
        self.assertEqual(result, point)
        
    def test_tuple_containing_namedtuples(self):
        """
        Test the case where tuples of namedtuples are processed
        This is directly related to what the bug report describes
        """
        Point = namedtuple('Point', ['x', 'y'])
        point1 = Point(1, 2)
        point2 = Point(3, 4)
        
        # This represents a tuple used for range filtering
        range_tuple = (point1, point2)
        
        from django.db.models.sql.query import Query
        query = Query(None)
        
        # This should work correctly with the fix
        result = query.resolve_lookup_value(range_tuple, can_reuse=[], allow_joins=True)
        self.assertEqual(result, range_tuple)