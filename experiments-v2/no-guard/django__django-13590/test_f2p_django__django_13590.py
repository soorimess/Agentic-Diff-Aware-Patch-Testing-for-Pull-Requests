from collections import namedtuple
from django.test import TestCase


class RangeFilterTest(TestCase):
    def test_namedtuple_range_filter(self):
        """Test that named tuples work as arguments to __range filters."""
        # Create a named tuple type
        Range = namedtuple('Range', ['start', 'end'])
        
        # This should work without raising TypeError
        # The bug was that named tuples would cause:
        # TypeError: __new__() missing 1 required positional argument: 'end'
        try:
            # Test the problematic code path directly
            from django.db.models.sql.query import Query
            
            # Create a mock model to satisfy Query initialization
            class MockModel:
                _meta = type('Meta', (), {'app_label': 'test'})()
            
            query = Query(MockModel)
            
            # This should not raise an exception
            range_value = Range(1, 10)
            result = query.resolve_lookup_value(range_value, can_reuse=[], allow_joins=True)
            
            # The result should be a Range namedtuple with resolved values
            self.assertIsInstance(result, Range)
            self.assertEqual(result.start, 1)
            self.assertEqual(result.end, 10)
            
        except TypeError as e:
            if "missing 1 required positional argument" in str(e):
                self.fail(f"Named tuple range filter failed with: {e}")
            raise

    def test_regular_tuple_range_filter(self):
        """Test that regular tuples still work (regression test)."""
        # Test with regular tuple
        from django.db.models.sql.query import Query
        
        # Create a mock model to satisfy Query initialization
        class MockModel:
            _meta = type('Meta', (), {'app_label': 'test'})()
        
        query = Query(MockModel)
        
        # This should work without raising an exception
        range_value = (1, 10)
        result = query.resolve_lookup_value(range_value, can_reuse=[], allow_joins=True)
        
        # The result should be a tuple with resolved values
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 10)