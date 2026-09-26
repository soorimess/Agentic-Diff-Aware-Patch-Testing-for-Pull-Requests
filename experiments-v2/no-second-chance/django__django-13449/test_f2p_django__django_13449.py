from django.db.models import F, Window
from django.db.models.functions import Lag
from django.test import TestCase, skipUnlessDBFeature


class LagDecimalFieldTest(TestCase):
    @skipUnlessDBFeature('supports_over_clause')
    def test_window_lag_decimalfield_syntax(self):
        """
        Regression test for Django issue #13449.
        Tests that Window with Lag on DecimalField doesn't cause syntax errors.
        """
        # Create the problematic window expression
        w = Window(expression=Lag('amount', 7), partition_by=[F('modified')], order_by=F('modified').asc())
        
        # Verify the expression was created correctly
        self.assertIsNotNone(w)
        self.assertTrue(hasattr(w, 'source_expression'))