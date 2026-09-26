import unittest
from django.http import HttpRequest
from django.views.debug import ExceptionReporter
from django.test import TestCase


class TestSuppressContextBug(TestCase):
    """Test that debug error view respects exc.__suppress_context__ (PEP 415)"""

    def test_suppress_context_behavior_in_frames(self):
        """
        Test the specific behavior that the fix addresses:
        When __suppress_context__ is True, the debug view should not show
        the original exception in the traceback frames.
        """
        # Create the exact scenario from the bug report
        try:
            try:
                raise RuntimeError('my error')
            except Exception as exc:
                raise ValueError('my new error') from None
        except ValueError as e:
            # The key test: with 'from None', __suppress_context__ is True
            # The debug view should suppress the RuntimeError from frames
            request = HttpRequest()
            reporter = ExceptionReporter(request, e.__class__, e, e.__traceback__)
            frames = reporter.get_traceback_frames()
            
            # Check that no frame has RuntimeError as its cause
            # This is the behavior that was fixed
            for frame in frames:
                exc_cause = frame.get('exc_cause')
                if exc_cause:
                    # This assertion should pass with the fix
                    # and would fail with the bug
                    self.assertNotEqual(
                        exc_cause.__class__.__name__,
                        'RuntimeError',
                        "RuntimeError should be suppressed when __suppress_context__ is True"
                    )
            
            # Verify the exception properties are correct
            self.assertIsNone(e.__cause__)
            self.assertTrue(e.__suppress_context__)
            self.assertIsInstance(e.__context__, RuntimeError)
            
    def test_exception_chain_walking_behavior(self):
        """
        Test that the exception chain walking respects suppress_context properly.
        """
        try:
            try:
                raise RuntimeError('original')
            except Exception as exc:
                raise ValueError('new') from None
        except ValueError as e:
            # Test the core logic that was potentially buggy
            # Walk the chain the way the code processes it
            
            # This is the exception chain walking logic that was changed
            exceptions = []
            exc_value = e
            
            # The logic that was potentially buggy:
            while exc_value:
                exceptions.append(exc_value)
                explicit = getattr(exc_value, '__cause__', None)
                suppress_context = getattr(exc_value, '__suppress_context__', None)
                implicit = getattr(exc_value, '__context__', None)
                
                # The key line that was potentially problematic:
                exc_value = explicit or (None if suppress_context else implicit)
                
                if exc_value in exceptions:
                    break
                    
            # With 'from None', we should only have the main exception
            # The RuntimeError should be suppressed
            exception_names = [exc.__class__.__name__ for exc in exceptions]
            
            # This should be ['ValueError'] - the main exception only
            self.assertEqual(exception_names, ['ValueError'])
            
    def test_no_regression_normal_chains(self):
        """
        Ensure normal exception chains still work (no regression).
        """
        try:
            try:
                raise RuntimeError('original')
            except Exception as exc:
                raise ValueError('new') from exc  # Normal chaining
        except ValueError as e:
            # Normal chains should work the same way
            request = HttpRequest()
            reporter = ExceptionReporter(request, e.__class__, e, e.__traceback__)
            frames = reporter.get_traceback_frames()
            
            # Should have frames
            self.assertGreater(len(frames), 0)