"""Regression test for pylint issue #6903.

This test ensures that _query_cpu function returns at least 1 CPU
when running in Kubernetes environments where CPU shares calculation
would otherwise return 0.
"""

from unittest.mock import patch, mock_open

from pylint.lint.run import _query_cpu


def test_query_cpu_zero_shares_returns_one():
    """Test that _query_cpu returns 1 when shares calculation would return 0.
    
    This is a regression test for issue where Kubernetes pods with
    cpu.shares=2 and cpu.cfs_period_us=100000 would cause _query_cpu
    to return 0, which would break multiprocessing.Pool.
    
    The calculation int(2 / 1024) = int(0.001953125) = 0
    But should return 1 to prevent multiprocessing failure.
    """
    # Mock the file operations to simulate the problematic scenario
    with patch('pathlib.Path.is_file') as mock_is_file:
        # Make cpu.shares file appear to exist (this is the path that causes the bug)
        mock_is_file.return_value = True
        
        # Mock open to return the problematic value: cpu.shares = 2
        with patch('builtins.open', mock_open(read_data="2")) as mock_file:
            # This should return 1 (not 0) after the fix is applied
            result = _query_cpu()
            
            # The fix ensures that when the calculation would return 0,
            # it returns 1 instead to prevent multiprocessing.Pool from failing
            assert result == 1, f"Expected 1 (to prevent multiprocessing failure), got {result}"