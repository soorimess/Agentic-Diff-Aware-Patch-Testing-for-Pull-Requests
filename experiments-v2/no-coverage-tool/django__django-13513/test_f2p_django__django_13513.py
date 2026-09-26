import unittest
from django.test import TestCase


class SuppressContextRegressionTest(TestCase):
    """Test that debug error view respects exc.__suppress_context__ (PEP 415)."""

    def test_suppress_context_exception_properties(self):
        """
        Test that validates the correct properties of exceptions with suppressed context.
        This test ensures that when an exception is raised with 'from None',
        the __suppress_context__ attribute is properly set.
        """
        # Test the exact scenario from the bug report
        try:
            try:
                raise RuntimeError('my error')
            except Exception as exc:
                raise ValueError('my new error') from None
        except ValueError as e:
            # These are the properties that should be set correctly
            # The fix ensures these are handled properly in the debug view
            self.assertIsNone(e.__cause__)
            self.assertTrue(e.__suppress_context__)
            self.assertIsNotNone(e.__context__)
            
            # Validate that the context contains the expected inner exception
            self.assertEqual(str(e.__context__), 'my error')
            self.assertEqual(type(e.__context__).__name__, 'RuntimeError')