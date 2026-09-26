import unittest
import sys
from django.views.debug import ExceptionReporter
from django.http import HttpRequest


class SuppressContextTest(unittest.TestCase):
    def test_debug_view_suppresses_context_correctly(self):
        """
        Test that Django debug view properly suppresses context when __suppress_context__ is True.
        
        This test specifically checks that when an exception is raised with 'from None',
        the debug view doesn't show the suppressed exception in the traceback frames.
        """
        # Create the exact scenario from the bug report
        try:
            try:
                raise RuntimeError('my error')
            except Exception as exc:
                raise ValueError('my new error') from None
        except Exception:
            exc_type, exc_value, tb = sys.exc_info()
        
        # Create ExceptionReporter (as used by Django debug view)
        request = HttpRequest()
        reporter = ExceptionReporter(request, exc_type, exc_value, tb)
        
        # Get traceback frames (this is what the debug view uses)
        frames = reporter.get_traceback_frames()
        
        # The core assertion: the debug view should NOT show RuntimeError
        # because ValueError was raised with 'from None' which suppresses context
        self.assertGreater(len(frames), 0, "Should have at least one frame")
        
        # Check that the first frame's exc_cause is None (context suppressed)
        first_frame = frames[0]
        exc_cause = first_frame.get('exc_cause')
        
        # This is the key assertion - in the buggy version this would fail
        # because exc_cause would be RuntimeError instead of None
        self.assertIsNone(exc_cause, 
                         "exc_cause should be None when __suppress_context__ is True "
                         "(exception raised with 'from None')")