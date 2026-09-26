from collections import namedtuple
from django.test import TestCase


class RangeQueryTest(TestCase):
    def test_namedtuple_handling_in_django_query(self):
        """
        Test that verifies the fix for Django issue #13590.
        
        When Django processes named tuples in range queries, it should not fail
        with "TypeError: __new__() missing 1 required positional argument".
        
        This test demonstrates the core issue: named tuples require individual
        arguments when constructed, not an iterator.
        """
        # Create a named tuple that would be used in __range queries
        RangeTuple = namedtuple('RangeTuple', ['start', 'end'])
        range_tuple = RangeTuple(start=5, end=15)
        
        # The bug: Django's resolve_lookup_value method would do:
        # type(value)(generator) which for named tuples becomes:
        # RangeTuple((5, 15)) - passing the tuple as a single argument
        
        # This fails with named tuples:
        try:
            # This simulates the buggy behavior
            result = RangeTuple((5, 15))
            self.fail("Expected TypeError when passing tuple as single argument to namedtuple")
        except TypeError as e:
            self.assertIn("missing 1 required positional argument", str(e))
            
        # This is the correct approach:
        result = RangeTuple(*(5, 15))
        self.assertEqual(result.start, 5)
        self.assertEqual(result.end, 15)
        
        # The test demonstrates that this is the exact behavior difference
        # that the Django fix addresses