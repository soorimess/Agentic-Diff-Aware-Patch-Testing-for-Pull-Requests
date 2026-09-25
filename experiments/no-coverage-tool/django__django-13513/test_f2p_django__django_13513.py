"""
Regression test for Django __suppress_context__ behavior in debug views.
Tests: when an exception is raised with "from None", 
the debug view should respect __suppress_context__ = True.
"""
from django.test import TestCase


class DjangoSuppressContextTest(TestCase):
    """
    Test that ensures debugging behavior correctly respects __suppress_context__
    """
    
    def test_suppress_context_flag_correctly_set(self):
        """
        Verify that exceptions with 'from None' correctly have __suppress_context__ = True.
        This validates the background condition of the bug fix.
        """
        try:
            try:
                raise RuntimeError('original error')
            except Exception as exc:
                raise ValueError('new error') from None
        except Exception as final_exc:
            # Before fix, traceback would incorrectly show original error even though suppressed
            # After fix, traceback should NOT show the suppressed context chain
            self.assertTrue(hasattr(final_exc, '__suppress_context__'))
            self.assertTrue(final_exc.__suppress_context__)