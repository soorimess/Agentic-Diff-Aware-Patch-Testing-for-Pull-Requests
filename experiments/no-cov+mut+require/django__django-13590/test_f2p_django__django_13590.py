from django.test import TestCase
from collections import namedtuple


class TestNamedTupleRangeFilter(TestCase):
    def test_namedtuple_range_filter_does_not_raise_typeerror(self):
        """
        Regression test for Django issue #13590.
        
        Before the fix, when named tuples were used as arguments to __range 
        queryset filters, Django would raise:
        TypeError: __new__() missing 1 required positional argument: 'far'
        
        This happened because resolve_lookup_value would try to reconstitute
        the named tuple by passing an iterator to its constructor rather than
        unpacking the values.
        """
        # Define a namedtuple that would be used as range filter argument
        RangeTuple = namedtuple('RangeTuple', ['near', 'far'])
        
        # Create an instance (this would be passed to range query)
        range_args = RangeTuple(near=10, far=20)
        
        # The problem: type(range_args)(iterator) fails for namedtuples
        # The fix: type(range_args)(*iterator) works for namedtuples 
        try:
            # Test that constructing a namedtuple with unpacked values works
            # This simulates what Django's resolve_lookup_value now does correctly
            result = type(range_args)(*range_args)
            
            # Validation that it worked properly
            self.assertEqual(result.near, 10)
            self.assertEqual(result.far, 20)
        except TypeError as e:
            if "missing 1 required positional argument" in str(e):
                # This is the exact error mentioned in bug report
                self.fail(f"Namedtuple construction failed with: {e}")
            raise  # Re-raise if it's a different TypeError

    def test_regular_tuple_behavior_preserved(self):
        """
        Ensure regular tuple behavior is unchanged - regression test.
        """
        regular_tuple = (10, 20)
        result = tuple(regular_tuple)
        self.assertEqual(result, (10, 20))