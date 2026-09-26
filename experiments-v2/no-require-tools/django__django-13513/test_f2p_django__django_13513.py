import sys
import unittest
from django.http import HttpRequest
from django.views.debug import ExceptionReporter


class TestSuppressContext(unittest.TestCase):
    """Test that debug error view respects exc.__suppress_context__ (PEP 415)"""

    def test_suppress_context_behavior(self):
        """
        The core test for the bug fix: when an exception is raised with 'from None',
        the debug view should respect __suppress_context__ and not show the original
        exception in the traceback.
        
        This test specifically verifies the behavior that was broken in the bug report.
        """
        # Exact scenario from the bug report
        def test_view():
            try:
                raise RuntimeError('my error')
            except Exception as exc:
                raise ValueError('my new error') from None

        try:
            test_view()
        except ValueError as e:
            # The bug: when ValueError is raised with 'from None', 
            # the original RuntimeError should not appear in the traceback
            # because __suppress_context__ is True
            
            exc_type, exc_value, tb = sys.exc_info()
            request = HttpRequest()
            reporter = ExceptionReporter(request, exc_type, exc_value, tb)
            frames = reporter.get_traceback_frames()
            
            # The key assertion: when __suppress_context__ is True (from None),
            # exc_cause should be None, not the RuntimeError
            self.assertGreater(len(frames), 0, "Should have traceback frames")
            
            # This is the specific behavior that was broken:
            # Old buggy code would return RuntimeError (the context) 
            # New correct code returns None (because __suppress_context__ is True)
            first_frame = frames[0]
            self.assertIsNone(first_frame['exc_cause'],
                            "When raised with 'from None', exc_cause must be None "
                            "to respect __suppress_context__")
            
            # Verify the underlying exception attributes are correct
            self.assertIsNone(getattr(e, '__cause__', None),
                            "ValueError from None should have __cause__ = None")
            self.assertTrue(getattr(e, '__suppress_context__', False),
                            "ValueError from None should have __suppress_context__ = True")

    def test_exception_chain_preservation(self):
        """
        Ensure normal exception chaining still works correctly.
        """
        def test_view():
            try:
                raise RuntimeError('original error')
            except Exception as exc:
                raise ValueError('new error') from exc

        try:
            test_view()
        except ValueError as e:
            exc_type, exc_value, tb = sys.exc_info()
            request = HttpRequest()
            reporter = ExceptionReporter(request, exc_type, exc_value, tb)
            frames = reporter.get_traceback_frames()
            
            # Should work normally without crashing
            self.assertGreater(len(frames), 0, "Should have traceback frames")