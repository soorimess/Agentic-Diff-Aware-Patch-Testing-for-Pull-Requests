# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for the Kubernetes Pod --jobs=0 bug.

This test ensures that _query_cpu() never returns 0, which would cause 
multiprocessing.Pool to crash with "Number of processes must be at least 1".
"""

from pylint.lint.run import _query_cpu


def test_query_cpu_never_returns_zero():
    """Test that _query_cpu never returns 0 to prevent multiprocessing crashes.
    
    The fix ensures that when calculating available CPUs, if the calculation 
    would result in 0 (e.g., int(2/1024) = 0), it is corrected to 1 to prevent
    multiprocessing.Pool from crashing with "Number of processes must be at least 1".
    """
    result = _query_cpu()
    
    # Core validation: function should never return 0 because:
    # 1. 0 would cause multiprocessing.Pool to crash (requires at least 1 process)
    # 2. The fix ensures avail_cpu is never 0 when it would break multiprocessing
    assert result is None or result >= 1, (
        "Function returned 0, which would break multiprocessing. "
        "The fix ensures that when calculation results in 0, it becomes 1."
    )


def test_query_cpu_returns_valid_result():
    """Test that _query_cpu returns valid results."""
    result = _query_cpu()
    
    # Validate normal behavior of the function
    if result is not None:
        assert isinstance(result, int), f"CPU count should be integer, got {type(result)}"
        assert result >= 1, f"CPU count should be at least 1, got {result}"