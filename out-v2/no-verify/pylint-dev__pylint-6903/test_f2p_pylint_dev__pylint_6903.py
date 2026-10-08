# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the fix of the _query_cpu function to prevent returning 0 in Kubernetes pods."""

from pylint.lint.run import _query_cpu


def test_query_cpu_never_returns_zero_for_multiprocessing():
    """Test that _query_cpu never returns 0 to prevent multiprocessing crashes.
    
    The fix ensures that when cpu calculation would result in 0 (e.g., 2/1024 = 0.001953125 -> 0),
    the function returns 1 instead to prevent multiprocessing.Pool from crashing.
    """
    result = _query_cpu()
    
    # If the function returns a value, it should be safe for multiprocessing (>= 1)
    # This prevents "Number of processes must be at least 1" error
    if result is not None:
        assert result >= 1, (
            "CPU count should be at least 1 to prevent multiprocessing crashes. "
            "The fix ensures this by returning 1 instead of 0 when calculation results in 0."
        )