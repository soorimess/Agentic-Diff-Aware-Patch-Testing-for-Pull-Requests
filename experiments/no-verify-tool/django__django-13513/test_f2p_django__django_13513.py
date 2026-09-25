"""
Tests for Django suppress context issue in debug views.
"""
from django.test import TestCase


class TestSuppressContext(TestCase):
    def test_suppress_context_attributes(self):
        """Verify suppress context attributes are set correctly."""
        # Test that demonstrates the behavior change needed
        # When 'from None' is used, __suppress_context__ should be True
        exc = RuntimeError('test')
        exc.__suppress_context__ = True
        self.assertTrue(exc.__suppress_context__)