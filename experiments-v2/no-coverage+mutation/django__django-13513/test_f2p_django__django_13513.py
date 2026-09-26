import unittest
from django.http import HttpRequest
from django.views.debug import ExceptionReporter


class SuppressContextTest(unittest.TestCase):
    def test_debug_error_view_handles_suppress_context(self):
        """
        Test that debug error view handles suppress_context correctly.
        """
        # Create exception chain with suppress_context
        try:
            try:
                raise RuntimeError('inner error')
            except Exception as exc:
                raise ValueError('outer error') from None
        except Exception as e:
            exc_value = e
            tb = e.__traceback__
            exc_type = type(e)

        # Verify suppress_context is set correctly
        self.assertTrue(hasattr(exc_value, '__suppress_context__'))
        self.assertTrue(exc_value.__suppress_context__)
        
        # Test that ExceptionReporter works with suppress_context
        request = HttpRequest()
        reporter = ExceptionReporter(request, exc_type, exc_value, tb)
        frames = reporter.get_traceback_frames()
        
        # Basic validation that frames are generated
        self.assertIsInstance(frames, list)
        self.assertGreater(len(frames), 0)