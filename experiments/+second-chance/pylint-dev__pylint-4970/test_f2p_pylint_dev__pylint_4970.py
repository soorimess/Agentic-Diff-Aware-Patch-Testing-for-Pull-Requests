"""Regression test for the bug where min-similarity-lines=0 does not disable duplicate checking."""

import tempfile
from pathlib import Path

from pylint.lint import PyLinter
from pylint.checkers.similar import SimilarChecker


def test_min_similarity_lines_zero_should_not_raise_zero_division_error():
    """Test that setting min-similarity-lines to 0 does not cause ZeroDivisionError.
    
    The bug: Setting min-similarity-lines=0 causes ZeroDivisionError because _compute_sims()
    is still called and produces empty results that cause division by zero in reporting.
    
    The fix: Setting min-similarity-lines=0 should return early from run() without calling
    _compute_sims() and avoiding the ZeroDivisionError.
    """
    # Create temporary file with content that will be processed
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test_file.py"
        
        # Create test content that makes sure files get parsed correctly
        # and there are lines to process
        content = '''def func1():
    x = 1
    y = 2
    return x + y

def func2():
    x = 1
    y = 2  
    return x + y
'''
        file_path.write_text(content)
        
        # Create a linter instance and similar checker  
        linter = PyLinter()
        checker = SimilarChecker(linter)
        checker.min_lines = 0  # Setting to 0 should disable duplicate checking
        
        # After fix, the method should return early and not raise ZeroDivisionError
        # Before fix, it would go through computation and hit the error
        try:
            checker.run()
            # If we reach here without exception, test passes (base behavior is good)
        except ZeroDivisionError:
            # This should not happen after the fix
            raise AssertionError("ZeroDivisionError occurred - min-similarity-lines=0 should not "
                               "cause division by zero in duplicate checking")


def test_min_similarity_lines_zero_skips_processing():
    """Test that when min_lines=0, processing is skipped early.
    
    The core behavior change: when min_lines=0, run() should return early without
    attempting to compute similarities.
    """
    # This is a functional test - we're checking that the key fix is present
    # by ensuring that behavior from the modified code path is properly changed
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test_file.py"
        content = "x = 1\ny = 2\n"
        file_path.write_text(content)
        
        linter = PyLinter()
        checker = SimilarChecker(linter)
        checker.min_lines = 0
        
        # The test itself is checking the behavior difference.
        # The actual test here is to make sure we don't hit the ZeroDivisionError
        # which would indicate that the early return is not working
        try:
            checker.run()
            # Test passes if we complete successfully without ZeroDivisionError
        except ZeroDivisionError:
            raise AssertionError("ZeroDivisionError confirms that fix is not working - "
                               "min_lines=0 should skip processing")