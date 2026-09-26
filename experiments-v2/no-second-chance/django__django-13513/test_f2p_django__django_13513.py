import unittest
from django.http import HttpRequest
from django.views.debug import ExceptionReporter


class SuppressContextTest(unittest.TestCase):
    def test_debug_view_respects_suppress_context(self):
        """
        Test that debug error view respects exc.__suppress_context__ (PEP 415).
        When an exception is raised with 'from None', the suppressed context 
        should not appear in the traceback frames.
        """
        # Create the exact scenario from the bug report
        try:
            try:
                raise RuntimeError('my error')
            except Exception as exc:
                raise ValueError('my new error') from None
        except Exception as final_exc:
            # Create the reporter
            request = HttpRequest()
            reporter = ExceptionReporter(request, type(final_exc), final_exc, final_exc.__traceback__)
            
            # Get traceback frames
            frames = reporter.get_traceback_frames()
            
            # Check if any frame shows RuntimeError as an exception cause
            # This would indicate the bug - RuntimeError should be suppressed
            for frame in frames:
                exc_cause = frame.get('exc_cause')
                if exc_cause is not None and type(exc_cause).__name__ == 'RuntimeError':
                    # This assertion fails when the bug exists
                    self.fail("RuntimeError should not appear as exception cause when suppressed with 'from None'")
            
            # Verify the structure
            self.assertEqual(type(final_exc).__name__, 'ValueError')
            self.assertTrue(getattr(final_exc, '__suppress_context__', False))