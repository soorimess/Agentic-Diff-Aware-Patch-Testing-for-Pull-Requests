"""
Regression test for Django ExpressionWrapper GROUP BY issue.

The issue was that ExpressionWrapper was missing get_group_by_cols() method.
Before fix:
- ExpressionWrapper would not delegate group_by_cols, causing constant expressions 
  in wrapped expressions to be incorrectly included in GROUP BY clauses

After fix:
- ExpressionWrapper properly delegates get_group_by_cols() to its wrapped expression
"""
from django.test import TestCase
from django.db.models import Value, IntegerField
from django.db.models.expressions import ExpressionWrapper


class ExpressionWrapperGroupByTest(TestCase):
    def test_expression_wrapper_properly_delegates_group_by_cols(self):
        """
        Test that ExpressionWrapper properly delegates get_group_by_cols() to 
        its wrapped expression to avoid incorrect GROUP BY clauses.
        
        Before fix: ExpressionWrapper(Value(3)) would return [ExpressionWrapper(Value(3))]
        After fix: ExpressionWrapper(Value(3)) should return [] (empty list)
        """
        # Create ExpressionWrapper around a constant value expression
        constant_expr = Value(3, output_field=IntegerField())
        wrapped_expr = ExpressionWrapper(constant_expr, output_field=IntegerField())
        
        # This is the key behavior change being tested
        group_by_cols = wrapped_expr.get_group_by_cols()
        
        # The behavior we're fixing:
        # - Constant expressions in GROUP BY cause PostgreSQL errors
        # - The fix prevents ExpressionWrapper from contributing itself to GROUP BY
        # - The expected result for a constant Value is an empty list
        self.assertEqual(group_by_cols, [], 
                        "ExpressionWrapper with constant must not contribute to GROUP BY")
        
        # Verify the wrapper method exists  
        self.assertTrue(hasattr(wrapped_expr, 'get_group_by_cols'))

    def test_inner_expression_group_by_cols_unchanged(self):
        """
        Ensure the wrapped expression's behavior is unchanged.
        """
        constant_expr = Value(3, output_field=IntegerField())
        
        # Verify that the wrapped expression itself behaves correctly
        group_by_cols = constant_expr.get_group_by_cols() 
        self.assertEqual(group_by_cols, [], 
                        "Constant Value expressions should not contribute to GROUP BY")