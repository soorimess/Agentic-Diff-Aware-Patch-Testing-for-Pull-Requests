"""
Regression test for Django issue where named tuples used as arguments to __range 
fail with TypeError in Django 3.0, working in Django 2.2.
"""
from django.test import SimpleTestCase
from collections import namedtuple


class TestRangeNamedTuple(SimpleTestCase):
    """Test that named tuples work correctly with range queries."""
    
    def test_named_tuple_range_lookup(self):
        """
        Test that named tuples are handled correctly in range lookup value processing.
        This specifically tests for the bug where named tuples would cause:
        TypeError: __new__() missing 1 required positional argument
        """
        # Import here to avoid model registration issues from multiple definitions
        from django.db.models.sql.query import Query
        from django.db import models
        
        # Define a model only once to avoid re-registration issues
        class TestModel(models.Model):
            class Meta:
                app_label = 'test'
        
        # Create a named tuple - this used to cause the TypeError 
        Point = namedtuple('Point', ['x', 'y'])
        point = Point(1, 10)
        
        # Create query object, which executes the resolve_lookup_value method
        query = Query(TestModel)
        
        # This should not fail with: TypeError: __new__() missing 1 required positional argument
        try:
            result = query.resolve_lookup_value(point, [], True)
            
            # If it does not fail, make sure we get the right output
            self.assertIsInstance(result, Point)
            self.assertEqual(result.x, 1)
            self.assertEqual(result.y, 10)
        except TypeError as e:
            if "missing 1 required positional argument" in str(e):
                self.fail(f"Named tuple not properly handled: {e}")
            raise