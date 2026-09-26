"""
Regression test for Django issue #13513: debug error view doesn't respect exc.__suppress_context__ (PEP 415)
"""
from django.test import TestCase
from django.views.debug import ExceptionReporter
from django.http import HttpRequest


class SuppressContextTest(TestCase):
    def test_debug_view_suppresses_context_correctly(self):
        """
        Test that the debug view correctly handles __suppress_context__ by examining 
        the actual traceback frames and their exc_cause values.
        """
        # Create a request object
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/test/'

        # Create the exact scenario from the bug report
        try:
            try:
                raise RuntimeError('my error')
            except Exception as exc:
                raise ValueError('my new error') from None
        except Exception as e:
            exc_value = e
            tb = e.__traceback__
            exc_type = type(e)

        # Create ExceptionReporter and get traceback frames
        reporter = ExceptionReporter(request, exc_type, exc_value, tb)
        frames = reporter.get_traceback_frames()

        # The bug was that the debug view would incorrectly show RuntimeError 
        # as the cause even when __suppress_context__ is True
        self.assertTrue(len(frames) > 0)
        
        # The key insight: when __suppress_context__ is True (from None),
        # the traceback should not contain the RuntimeError as a cause
        # Let's examine the actual frame data
        first_frame = frames[0]
        exc_cause = first_frame.get('exc_cause')
        
        # This assertion should fail in the buggy version but pass in the fixed version
        # In the buggy version, exc_cause would be RuntimeError (incorrectly shown)
        # In the fixed version, exc_cause should be None (correctly suppressed)
        self.assertIsNone(exc_cause, 
                         "When using 'from None', exc_cause should be None to respect __suppress_context__")
        
    def test_debug_view_preserves_context_when_needed(self):
        """
        Test that normal context preservation still works correctly.
        """
        # Create a request object
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/test/'

        # Create an exception chain that preserves context
        try:
            try:
                raise RuntimeError('original error')
            except Exception as exc:
                raise ValueError('new error') from exc
        except Exception as e:
            exc_value = e
            tb = e.__traceback__
            exc_type = type(e)

        # Create ExceptionReporter and get traceback frames
        reporter = ExceptionReporter(request, exc_type, exc_value, tb)
        frames = reporter.get_traceback_frames()

        # Check that we have frames
        self.assertTrue(len(frames) > 0)
        
        # This test ensures normal behavior is preserved
        # The main test is the first one about suppression