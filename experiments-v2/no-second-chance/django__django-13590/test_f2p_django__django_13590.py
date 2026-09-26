from collections import namedtuple
from django.test import TestCase


class TestNamedTupleRangeFilter(TestCase):
    def test_namedtuple_range_filter(self):
        """
        Test that named tuples work as arguments to __range filters.
        This is a regression test for Django issue #13590.
        """
        # Create a named tuple with two values (like what would be used in range filters)
        RangeTuple = namedtuple('RangeTuple', ['low', 'high'])
        range_values = RangeTuple(low=10, high=20)
        
        # Test the specific issue: when resolve_lookup_value processes a named tuple,
        # it should not fail with "__new__() missing 1 required positional argument"
        try:
            # Import the method directly to test it
            from django.db.models.sql.query import Query
            
            # Create a minimal query object for testing
            class MockQuery(Query):
                def __init__(self):
                    pass
                
                def get_meta(self):
                    class MockMeta:
                        def __init__(self):
                            self.model = None
                    return MockMeta()
            
            query = MockQuery()
            
            # This should trigger the problematic code path in resolve_lookup_value
            # The key is that when it tries to reconstruct the named tuple,
            # it should not fail with the TypeError
            result = query.resolve_lookup_value(range_values, can_reuse=[], allow_joins=True)
            
            # Verify the result is what we expect
            self.assertIsInstance(result, RangeTuple)
            self.assertEqual(result.low, 10)
            self.assertEqual(result.high, 20)
            
        except TypeError as e:
            # If we get the specific error mentioned in the bug report, this is the bug
            if "__new__() missing 1 required positional argument" in str(e):
                self.fail("Named tuple range filter failed with TypeError: %s" % e)
            else:
                raise

    def test_regular_tuple_behavior(self):
        """
        Test that regular tuples still work correctly.
        """
        # Create a regular tuple
        range_values = (10, 20)
        
        try:
            # Import the method directly to test it
            from django.db.models.sql.query import Query
            
            # Create a minimal query object for testing
            class MockQuery(Query):
                def __init__(self):
                    pass
                
                def get_meta(self):
                    class MockMeta:
                        def __init__(self):
                            self.model = None
                    return MockMeta()
            
            query = MockQuery()
            
            # This should work fine
            result = query.resolve_lookup_value(range_values, can_reuse=[], allow_joins=True)
            
            # Verify the result is what we expect
            self.assertIsInstance(result, tuple)
            self.assertEqual(result[0], 10)
            self.assertEqual(result[1], 20)
            
        except TypeError as e:
            # If we get a TypeError, it should not be the namedtuple error
            if "__new__() missing 1 required positional argument" in str(e):
                self.fail("Regular tuple test failed with TypeError: %s" % e)
            else:
                raise