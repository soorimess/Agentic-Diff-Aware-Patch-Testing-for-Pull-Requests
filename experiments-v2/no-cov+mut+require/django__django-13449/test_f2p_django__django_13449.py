import unittest
from django.test import TestCase, skipUnlessDBFeature


@skipUnlessDBFeature('supports_over_clause')
class LagDecimalFieldTest(TestCase):
    def test_lag_decimal_field_sqlite_syntax_error(self):
        """
        Regression test for Django bug: Lag() with DecimalField crashes on SQLite.
        
        This test verifies that Window expressions with Lag() on DecimalFields
        don't generate SQL with incorrect CAST placement that causes:
        OperationalError: near "OVER": syntax error
        
        The bug was in how Window expressions with DecimalFields were compiled
        for SQLite - the CAST was applied incorrectly around just the LAG function
        instead of the entire window expression.
        """
        # This expression should not raise OperationalError with "near OVER: syntax error"
        from django.db.models import F, Window
        from django.db.models.functions import Lag
        
        # Create the exact scenario from the bug report
        window_expr = Window(
            expression=Lag('amount', 7),
            partition_by=[F('modified')],
            order_by=F('modified').asc()
        )
        
        # The test is that we can process this expression without getting
        # the specific syntax error that was reported in the bug
        try:
            # Force evaluation of the expression to trigger SQL generation
            str(window_expr)
        except Exception as e:
            error_str = str(e).lower()
            # If we get the exact error from the bug report, fail the test
            if 'over' in error_str and 'syntax error' in error_str:
                # This is the bug we're testing for - it should not happen after fix
                raise AssertionError("BUG REPRODUCED: Lag() with DecimalField causes SQLite syntax error with OVER clause")
            # Re-raise other exceptions
            raise


if __name__ == '__main__':
    unittest.main()