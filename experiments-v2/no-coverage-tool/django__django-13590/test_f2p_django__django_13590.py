from collections import namedtuple
from django.db import models
from django.test import TestCase


class RangeModel(models.Model):
    value = models.IntegerField()

    class Meta:
        app_label = 'test'


class NamedTupleRangeTest(TestCase):
    def test_namedtuple_range_lookup(self):
        """
        Test that named tuples can be used as arguments to __range lookups.
        This is a regression test for Django issue #13590.
        """
        # Create a named tuple with required fields for range lookup
        Range = namedtuple('Range', ['near', 'far'])
        range_tuple = Range(5, 15)
        
        # This should not raise a TypeError about missing positional arguments
        # The bug was that named tuples would fail when used in __range lookups
        try:
            # This should work - it's a simple range lookup
            result = RangeModel.objects.filter(value__range=range_tuple)
            # If we get here without exception, the test passes
            self.assertIsInstance(result, models.QuerySet)
        except TypeError as e:
            if "missing 1 required positional argument" in str(e):
                self.fail("Named tuple range lookup failed with TypeError: %s" % e)
            raise

    def test_namedtuple_range_lookup_with_different_fields(self):
        """
        Test named tuple range lookup with different field names.
        """
        # Create a named tuple with different field names
        CustomRange = namedtuple('CustomRange', ['start', 'end'])
        range_tuple = CustomRange(10, 20)
        
        try:
            result = RangeModel.objects.filter(value__range=range_tuple)
            self.assertIsInstance(result, models.QuerySet)
        except TypeError as e:
            if "missing 1 required positional argument" in str(e):
                self.fail("Named tuple range lookup failed with TypeError: %s" % e)
            raise

    def test_regular_tuple_still_works(self):
        """
        Ensure regular tuples still work (regression test).
        """
        # Regular tuple should continue to work
        regular_tuple = (5, 15)
        
        try:
            result = RangeModel.objects.filter(value__range=regular_tuple)
            self.assertIsInstance(result, models.QuerySet)
        except Exception as e:
            self.fail("Regular tuple range lookup failed: %s" % e)

    def test_list_still_works(self):
        """
        Ensure lists still work (regression test).
        """
        # Regular list should continue to work
        regular_list = [5, 15]
        
        try:
            result = RangeModel.objects.filter(value__range=regular_list)
            self.assertIsInstance(result, models.QuerySet)
        except Exception as e:
            self.fail("List range lookup failed: %s" % e)