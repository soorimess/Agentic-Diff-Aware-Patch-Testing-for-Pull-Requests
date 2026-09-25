"""
Regression test for Django issue where debug error view doesn't respect
exc.__suppress_context__ (PEP 415).

The bug was in how get_traceback_frames() handled the resolution of chained 
exceptions when __suppress_context__ was True.
"""
from django.http import HttpRequest
from django.test import SimpleTestCase
from django.views.debug import ExceptionReporter


class TestSuppressContextRegression(SimpleTestCase):
    def test_exception_chain_suppression(self):
        """
        When an exception is raised with 'from None', __suppress_context__ 
        should cause the chained exception to be suppressed in debug view.
        """
        # Exactly reproduce the scenario from bug report  
        try:
            try:
                raise RuntimeError('my error')
            except Exception as exc:
                raise ValueError('my new error') from None
        except Exception as e:
            exc_value = e
            exc_type = type(e)
            tb = e.__traceback__

        # This will work correctly now (the bug is fixed) 
        # but the test shows the expected behavior
        
        # The key assertion we can make about what is SUPPOSED to happen:
        # When __suppress_context__ = True, there should be no exc_cause in the frame
        reporter = ExceptionReporter(HttpRequest(), exc_type, exc_value, tb)
        frames = reporter.get_traceback_frames()
        
        # Specify the behavior that should be tested - should be 1 frame (the ValueError)
        # and that frame should have exc_cause = None, not RuntimeError
        self.assertEqual(len(frames), 1)
        
        # The easy-to-check condition is that the frame doesn't show the RuntimeError context  
        if len(frames) > 0:
            frame = frames[0]
            exc_cause = frame.get('exc_cause', None)
            # This should be None because we suppressed the context
            # Before the fix, this would be RuntimeError('my error')
            self.assertIsNone(exc_cause, 
                "In suppressed exception context, exc_cause should be None, not the suppressed exception")
            
    def test_normal_chaining_unchanged(self):
        """
        Normal exception chaining without 'from None' should continue to work.
        """
        try:
            try:
                raise RuntimeError('original error')
            except Exception as exc:
                raise ValueError('new error') from exc
        except Exception as e:
            exc_value = e
            exc_type = type(e)
            tb = e.__traceback__

        reporter = ExceptionReporter(HttpRequest(), exc_type, exc_value, tb)
        frames = reporter.get_traceback_frames()
        
        # This could be 2 frames or more, depending on how the frames are structured 
        # Generally should be more than 1 when chaining normally  
        self.assertGreater(len(frames), 1, 
                          "Normal exception chain should create multiple frames")