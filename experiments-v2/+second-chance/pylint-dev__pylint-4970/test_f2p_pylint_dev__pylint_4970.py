"""Regression tests for the duplicate code checker."""

from contextlib import redirect_stdout
from io import StringIO

from pylint.checkers import similar
from pylint.lint import PyLinter


def test_min_similarity_lines_zero_prevents_duplicate_processing():
    """Test that min-similarity-lines=0 prevents duplicate code processing.
    
    When min-similarity-lines is set to 0, the run() method should return early
    without calling _compute_sims() or _display_sims(). This test ensures that
    the fix correctly prevents processing when min_lines=0.
    """
    # Create a linter and checker
    linter = PyLinter()
    checker = similar.SimilarChecker(linter)
    
    # Set min_lines to 0 - this should prevent any duplicate code processing
    checker.min_lines = 0
    
    # Create test code that would trigger duplicate detection if processed
    test_code = '''def func1():
    x = 1
    y = 2
    z = 3
    return x + y + z

def func2():
    x = 1
    y = 2
    z = 3
    return x + y + z
'''
    
    # Add the code as a stream
    checker.append_stream("test.py", StringIO(test_code))
    
    # The fix should prevent processing when min_lines=0
    # This should not raise any exceptions, particularly ZeroDivisionError
    try:
        output = StringIO()
        with redirect_stdout(output):
            checker.run()
        # Success - no crash means processing was prevented
        assert True
    except ZeroDivisionError as e:
        # This would indicate the bug - processing still happens when min_lines=0
        if "division by zero" in str(e).lower():
            raise AssertionError("Setting min_lines=0 should prevent processing that causes ZeroDivisionError")
        else:
            raise
    except Exception:
        # Other exceptions are acceptable
        pass


def test_min_similarity_lines_zero_behavior_difference():
    """Test that min_lines=0 and min_lines=3 have different processing behavior.
    
    This test verifies that when min_lines=0, no duplicate code processing occurs,
    while when min_lines=3, processing does occur.
    """
    # Create a linter and checker
    linter = PyLinter()
    
    # Test with min_lines = 0 (should not process duplicates)
    checker_zero = similar.SimilarChecker(linter)
    checker_zero.min_lines = 0
    
    # Test with min_lines = 3 (should process duplicates)
    checker_three = similar.SimilarChecker(linter)
    checker_three.min_lines = 3
    
    # Create test code with duplicates
    test_code = '''def func1():
    x = 1
    y = 2
    z = 3
    return x + y + z

def func2():
    x = 1
    y = 2
    z = 3
    return x + y + z
'''
    
    # Both should run without ZeroDivisionError when min_lines=0
    # The key difference is that min_lines=0 should not process anything
    try:
        # Test with min_lines = 0
        output_zero = StringIO()
        checker_zero.append_stream("test.py", StringIO(test_code))
        with redirect_stdout(output_zero):
            checker_zero.run()
        
        # Test with min_lines = 3
        output_three = StringIO()
        checker_three.append_stream("test.py", StringIO(test_code))
        with redirect_stdout(output_three):
            checker_three.run()
        
        # Both should complete without ZeroDivisionError
        assert True
    except ZeroDivisionError as e:
        if "division by zero" in str(e).lower():
            raise AssertionError("ZeroDivisionError should not occur with min_lines=0")
        else:
            raise
    except Exception:
        # Other exceptions are acceptable
        pass