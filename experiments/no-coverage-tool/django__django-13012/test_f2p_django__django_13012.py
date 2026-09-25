"""
Regression test for Django issue where ExpressionWrapper with constant expressions
incorrectly places those expressions in GROUP BY clause.
"""
from django.db.models import ExpressionWrapper, IntegerField, Value
from django.test import TestCase


class ExpressionWrapperGroupByTests(TestCase):
    def test_expression_wrapper_group_by_cols_delegation(self):
        """
        Test that ExpressionWrapper properly delegates get_group_by_cols to 
        its inner expression, which is critical for correct SQL GROUP BY generation.
        
        This addresses the specific issue where constant expressions in 
        ExpressionWrapper would incorrectly be included in GROUP BY clauses.
        
        Before fix: ExpressionWrapper would not have get_group_by_cols method,
        incorrectly including constants in GROUP BY.
        
        After fix: ExpressionWrapper.get_group_by_cols() delegates to 
        the inner expression's get_group_by_cols(), ensuring constants don't 
        appear in GROUP BY.
        """
        # Create a constant value expression that should not contribute to GROUP BY
        value_expr = Value(3)
        wrapper_expr = ExpressionWrapper(value_expr, output_field=IntegerField())
        
        # The Value expression's group by columns should be empty (constants don't group)
        value_group_by_cols = value_expr.get_group_by_cols()
        
        # The ExpressionWrapper's get_group_by_cols should delegate properly
        # This is the key test: it should be equivalent to the underlying expression
        wrapper_group_by_cols = wrapper_expr.get_group_by_cols()
        
        # Both should be empty since Value(3) is a constant expression
        self.assertEqual(len(value_group_by_cols), 0)
        self.assertEqual(len(wrapper_group_by_cols), 0)
        
        # Verify they're equivalent (same behavior)
        self.assertEqual(value_group_by_cols, wrapper_group_by_cols)
        
        # Verify the specific behavior we're fixing
        # Before fix, wrapper_group_by_cols would contain the constant value expression
        # After fix, wrapper_group_by_cols should be empty like value_group_by_cols
        self.assertEqual(wrapper_group_by_cols, [])
        
        # Test with explicit alias parameter to ensure delegation works properly
        wrapper_group_by_cols_with_alias = wrapper_expr.get_group_by_cols(alias='test_alias')
        value_group_by_cols_with_alias = value_expr.get_group_by_cols(alias='test_alias')
        
        # Both should behave identically 
        self.assertEqual(value_group_by_cols_with_alias, wrapper_group_by_cols_with_alias)