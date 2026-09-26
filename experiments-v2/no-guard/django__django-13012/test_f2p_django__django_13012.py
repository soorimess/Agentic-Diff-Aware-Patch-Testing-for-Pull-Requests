import unittest

from django.db.models import ExpressionWrapper, Value, IntegerField
from django.test import TestCase


class Django13012Test(TestCase):
    def test_expression_wrapper_get_group_by_cols_for_constant(self):
        """
        Test that ExpressionWrapper properly delegates get_group_by_cols to wrapped constant expression.
        
        Regression test for Django #13012.
        """
        # Create a constant expression (Value) that should not be in GROUP BY
        constant_expr = Value(3, output_field=IntegerField())
        
        # Test that Value directly returns empty group by cols (this should work)
        direct_group_by_cols = constant_expr.get_group_by_cols()
        self.assertEqual(len(direct_group_by_cols), 0, 
                        "Value expression should not produce group by columns")
        
        # Wrap it in ExpressionWrapper
        wrapped_expr = ExpressionWrapper(constant_expr, output_field=IntegerField())
        
        # Test that get_group_by_cols method exists and works correctly
        # Before the fix, this would fail or return incorrect results
        try:
            # This should not raise an exception and should properly delegate
            group_by_cols = wrapped_expr.get_group_by_cols()
            # The constant Value(3) should not produce any group by columns
            # This assertion will fail before the fix because ExpressionWrapper doesn't have get_group_by_cols
            self.assertEqual(len(group_by_cols), 0,
                            "ExpressionWrapper with constant should not produce group by columns")
        except AttributeError as e:
            # If get_group_by_cols doesn't exist, that's the bug
            if "get_group_by_cols" in str(e):
                self.fail("ExpressionWrapper missing get_group_by_cols method - this is the bug!")
            raise
        except Exception as e:
            self.fail(f"Unexpected error in get_group_by_cols: {e}")