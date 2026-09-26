# Copyright (c) 2023, 2024 PyCQA and contributors
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Regression test for issue #4970 - Setting min-similarity-lines to 0 should disable duplicate code checking."""

from pylint.checkers import similar
from pylint.lint import PyLinter


def test_min_similarity_lines_zero_should_return_early():
    """Test that SimilarChecker.run() returns early when min_lines is 0 to prevent ZeroDivisionError.
    
    Before the fix, setting min-similarity-lines to 0 would cause a ZeroDivisionError
    because the code would still try to compute similarities and then divide by zero
    when calculating percentages. The fix adds an early return when min_lines == 0.
    """
    # Create a linter instance
    linter = PyLinter()
    
    # Create a SimilarChecker instance directly
    checker = similar.SimilarChecker(linter)
    checker.min_lines = 0  # This should cause the checker to return early
    
    # The key test: when min_lines == 0, run() should return immediately
    # without trying to compute similarities that would cause a ZeroDivisionError
    try:
        checker.run()
        # If we get here without error, the fix works
        assert True
    except ZeroDivisionError as e:
        # This would happen if the fix isn't applied and _compute_sims() is called
        if "division by zero" in str(e):
            raise AssertionError("Fix not applied: SimilarChecker.run() with min_lines=0 still tries to compute similarities and crashes")
        raise
    except Exception as e:
        # Any other exception is unexpected
        raise AssertionError(f"Unexpected error when running SimilarChecker with min_lines=0: {e}")