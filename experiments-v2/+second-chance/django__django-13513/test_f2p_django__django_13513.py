import unittest
import sys
from django.test import RequestFactory
from django.views.debug import ExceptionReporter


class TestSuppressContext(unittest.TestCase):
    """Test that debug error view respects exc.__suppress_context__ (PEP 415)"""

    def test_suppress_context_behavior(self):
        """
        When using 'from None', suppressed exceptions should not appear in traceback.
        """
        factory = RequestFactory()
        request = factory.get('/test/')
        
        try:
            try:
                raise RuntimeError('inner')
            except Exception as exc:
                raise ValueError('outer') from None
        except Exception as final_exc:
            reporter = ExceptionReporter(request, type(final_exc), final_exc, sys.exc_info()[2])
            frames = reporter.get_traceback_frames()
            
            # Check that RuntimeError is NOT in any frame's exception cause
            # This is the core assertion that should fail on buggy code
            for frame in frames:
                exc_cause = frame.get('exc_cause')
                if exc_cause is not None:
                    self.assertNotEqual(type(exc_cause).__name__, 'RuntimeError')

    def test_normal_chaining_preserved(self):
        """
        Normal exception chaining should still work.
        """
        factory = RequestFactory()
        request = factory.get('/test/')
        
        try:
            try:
                raise RuntimeError('inner')
            except Exception as exc:
                raise ValueError('outer') from exc
        except Exception as final_exc:
            reporter = ExceptionReporter(request, type(final_exc), final_exc, sys.exc_info()[2])
            frames = reporter.get_traceback_frames()
            
            # Check that RuntimeError IS in some frame's exception cause
            has_runtime_error = False
            for frame in frames:
                exc_cause = frame.get('exc_cause')
                if exc_cause is not None and type(exc_cause).__name__ == 'RuntimeError':
                    has_runtime_error = True
                    break
                    
            self.assertTrue(has_runtime_error)