"""
Regression test for Django issue #13513:
Debug error view doesn't respect exc.__suppress_context__ (PEP 415)
"""
import sys
from django.test import SimpleTestCase
from django.views.debug import ExceptionReporter


class DebugSuppressContextTest(SimpleTestCase):
    def test_suppressed_exception_not_in_html(self):
        """
        Test that when an exception is raised with 'from None',
        the debug HTML does not contain the original exception message.
        """
        # Create the exact scenario from the bug report
        try:
            try:
                raise RuntimeError('my error')
            except Exception as exc:
                raise ValueError('my new error') from None
        except ValueError:
            exc_type, exc_value, tb = sys.exc_info()

        # Create an exception reporter and get HTML traceback
        reporter = ExceptionReporter(None, exc_type, exc_value, tb)
        html = reporter.get_traceback_html()
        
        # The bug is that HTML contains "my error" (the RuntimeError) 
        # even though it was suppressed with 'from None'
        # This test should fail on buggy code and pass on fixed code
        self.assertNotIn('my error', html, 
                       "RuntimeError should not appear in HTML when suppressed with 'from None'")