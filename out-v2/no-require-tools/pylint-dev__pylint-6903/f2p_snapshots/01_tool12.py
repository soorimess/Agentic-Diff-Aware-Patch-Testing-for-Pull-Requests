# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the _query_cpu function bug fix.

This test ensures that when _query_cpu() calculates a value of 0 due to
Kubernetes pod fractional CPU resources, it returns 1 instead to avoid
multiprocessing failures.
"""

# pylint: disable=protected-access,missing-function-docstring

import sys
from unittest.mock import patch

from pylint.lint.run import _query_cpu


def test_query_cpu_zero_fractional_k8s():
    """Test that _query_cpu returns 1 when calculation would yield 0 in Kubernetes.
    
    This reproduces the bug where Kubernetes pods with fractional CPU resources
    cause _query_cpu to return 0, which breaks multiprocessing.Pool.
    
    The bug occurs when:
    - cpu.cfs_quota_us = -1 (so quota != -1 condition fails)  
    - cpu.shares = 2 (which leads to int(2/1024) = 0)
    """
    # Test the specific calculation that causes the issue
    # We'll directly test the logic by mocking the file system calls
    
    # Mock the Path.is_file method to make all cgroup files appear to exist
    with patch('pylint.lint.run.Path.is_file') as mock_is_file:
        # Make all cgroup files appear to exist
        mock_is_file.return_value = True
        
        # Mock the open function to return our test values
        with patch('pylint.lint.run.open') as mock_open:
            # Create mock file objects that return our test values
            def mock_file_content(path):
                if str(path) == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
                    return "-1\n"
                elif str(path) == "/sys/fs/cgroup/cpu/cpu.cfs_period_us":
                    return "100000\n"
                elif str(path) == "/sys/fs/cgroup/cpu/cpu.shares":
                    return "2\n"
                return ""
            
            # Create a mock file object
            class MockFile:
                def __init__(self, path, *args, **kwargs):
                    self.path = path
                    self.content = mock_file_content(path)
                
                def __enter__(self):
                    return self
                
                def __exit__(self, *args):
                    pass
                
                def read(self):
                    return self.content
                
                def readline(self):
                    return self.content
                
                def close(self):
                    pass
            
            mock_open.side_effect = MockFile
            
            # Call the function
            result = _query_cpu()
            
            # Before the fix, this would return 0
            # After the fix, this should return 1
            assert result == 1, f"Expected 1 (fixed behavior), got {result}"


def test_query_cpu_zero_case():
    """Test that _query_cpu returns 1 when shares calculation results in 0."""
    # This specifically tests the fix for the zero case
    with patch('pylint.lint.run.Path.is_file') as mock_is_file:
        # Make all cgroup files appear to exist
        mock_is_file.return_value = True
        
        # Mock the open function to return our test values
        with patch('pylint.lint.run.open') as mock_open:
            # Create mock file objects that return our test values
            def mock_file_content(path):
                if str(path) == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
                    return "-1\n"  # This makes it skip the quota/period path
                elif str(path) == "/sys/fs/cgroup/cpu/cpu.shares":
                    return "2\n"   # This causes int(2/1024) = 0
                return ""
            
            # Create a mock file object
            class MockFile:
                def __init__(self, path, *args, **kwargs):
                    self.path = path
                    self.content = mock_file_content(path)
                
                def __enter__(self):
                    return self
                
                def __exit__(self, *args):
                    pass
                
                def read(self):
                    return self.content
                
                def readline(self):
                    return self.content
                
                def close(self):
                    pass
            
            mock_open.side_effect = MockFile
            
            # Call the function
            result = _query_cpu()
            
            # This should be 1 after the fix (not 0)
            assert result == 1, f"Expected 1 (fixed behavior), got {result}"


def test_query_cpu_normal_case():
    """Test that _query_cpu works normally for typical cases."""
    # Test with a normal case where shares > 1024 to get a reasonable number
    with patch('pylint.lint.run.Path.is_file') as mock_is_file:
        # Make all cgroup files appear to exist
        mock_is_file.return_value = True
        
        # Mock the open function to return our test values
        with patch('pylint.lint.run.open') as mock_open:
            # Create mock file objects that return our test values
            def mock_file_content(path):
                if str(path) == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
                    return "-1\n"  # Skip quota/period path
                elif str(path) == "/sys/fs/cgroup/cpu/cpu.shares":
                    return "2048\n"  # This should give 2 CPUs (2048/1024 = 2)
                return ""
            
            # Create a mock file object
            class MockFile:
                def __init__(self, path, *args, **kwargs):
                    self.path = path
                    self.content = mock_file_content(path)
                
                def __enter__(self):
                    return self
                
                def __exit__(self, *args):
                    pass
                
                def read(self):
                    return self.content
                
                def readline(self):
                    return self.content
                
                def close(self):
                    pass
            
            mock_open.side_effect = MockFile
            
            # Call the function
            result = _query_cpu()
            
            # Should return 2 for 2048 shares / 1024
            assert result == 2, f"Expected 2, got {result}"