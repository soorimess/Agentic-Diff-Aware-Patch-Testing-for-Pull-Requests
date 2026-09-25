"""
Regression test for Django issue: named tuples used as arguments to __range 
should not error when upgrading from 2.2 to 3.0
"""

from collections import namedtuple
from django.test import TestCase


class TestNamedTupleRange(TestCase):
    def test_namedtuple_range_filter(self):
        """
        Test that named tuples work as arguments to range queryset filters.
        
        This simulates the issue where Django 2.2 works fine with named tuples
        but Django 3.0 would error with "TypeError: __new__() missing 1 required 
        positional argument: 'far'". 
        """
        # Create named tuple type - should be the same as how the bug happens
        RangeTuple = namedtuple('RangeTuple', ['start', 'end'])
        
        # Create instance of named tuple
        test_tuple = RangeTuple(10, 20)
        
        # Test direct resolve_lookup_value functionality
        # We will test this by triggering the code path that causes the issue
        from django.db.models.sql.query import Query
        from django.db import models
        
        class RangeTestModel(models.Model):
            name = models.CharField(max_length=100)
            value = models.IntegerField()
            
            class Meta:
                app_label = 'test'
        
        # Create a query object to directly test resolve_lookup_value
        query = Query(RangeTestModel)
        
        # This should exercise the problem - passing a named tuple to the 
        # resolve_lookup_value method which internally attempts to recreate 
        # the tuple using type(value)() with a generator expression
        try:
            result = query.resolve_lookup_value(test_tuple, can_reuse=[], allow_joins=True)
            # If we get here, the fix may already be in place
            # Verify it's the correct result type and values
            self.assertIsInstance(result, RangeTuple)
            self.assertEqual(result.start, 10)
            self.assertEqual(result.end, 20)
        except TypeError as e:
            # This should be the error in the old buggy version but should not occur after fix
            if "__new__() missing 1 required positional argument" in str(e):
                self.fail("Found original bug: %s" % str(e))
            else:
                raise  # Re-raise if it's a different TypeError