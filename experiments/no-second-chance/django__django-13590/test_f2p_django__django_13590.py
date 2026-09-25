"""
Regression test for Django issue #13590.

Tests the exact behavior fix in resolve_lookup_value for named tuples.
"""
from collections import namedtuple
from django.test import TestCase


class TestRangeNamedTuple(TestCase):
    def test_named_tuple_handling_bug(self):
        """
        Test that named tuples are properly handled by resolve_lookup_value.
        
        This test directly targets the bug reported: when resolve_lookup_value tries
        to reconstruct a named tuple from iterated values, it fails because the 
        old code was: return type(value)(generator)
        But named tuples don't accept generators in their constructor.
        """
        # Create a named tuple like the Django filters would use
        RangeTuple = namedtuple('RangeTuple', ['low', 'high'])
        range_tuple = RangeTuple(1, 10)

        # Simulate what happens with nested resolution
        from django.db.models.sql.query import Query
        from django.db import models

        # We can only call resolve_lookup_value with a valid model context
        class DummyModel(models.Model):
            class Meta:
                app_label = 'admin'

        query = Query(DummyModel)
        
        # The actual test call that would fail in old code
        try:
            result = query.resolve_lookup_value(range_tuple, can_reuse=[], allow_joins=True)
            # If we get here, it succeeded
            self.assertIsInstance(result, RangeTuple)
            self.assertEqual(result.low, 1)
            self.assertEqual(result.high, 10)
        except TypeError as e:
            # Check if it's the exact bug we're fixing
            if "__new__() missing 1 required positional argument:" in str(e):
                self.fail(f"Named tuple resolve bug reproduced: {e}")
            else:
                # Some other TypeError - not our target bug
                raise

    def test_regular_tuple_fallback_behavior(self):
        """
        Test that regular tuples still work correctly (cover the fallback path).
        
        This ensures line 1087 of the fix is covered: when processing regular tuples,
        not named tuples, the code should use: return type_(values) not return type_(*values)  
        """
        from django.db.models.sql.query import Query
        from django.db import models

        # We can only call resolve_lookup_value with a valid model context
        class DummyModel(models.Model):
            class Meta:
                app_label = 'admin'

        query = Query(DummyModel)
        
        # Test with regular tuple - this should exercise the fallback path
        regular_tuple = (1, 10)
        
        try:
            result = query.resolve_lookup_value(regular_tuple, can_reuse=[], allow_joins=True)
            self.assertIsInstance(result, tuple)
            self.assertEqual(result[0], 1)
            self.assertEqual(result[1], 10)
        except Exception as e:
            self.fail(f"Regular tuple processing failed: {e}")