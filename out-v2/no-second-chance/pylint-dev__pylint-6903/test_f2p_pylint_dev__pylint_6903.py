# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint issue #6903.

This test ensures that _query_cpu() returns at least 1 when the calculation
would otherwise return 0, preventing crashes in Kubernetes environments.
"""

import os
import tempfile
from pathlib import Path
from unittest import mock

from pylint.lint.run import _query_cpu


def test_query_cpu_zero_shares_returns_one():
    """Test that _query_cpu returns 1 when shares calculation would result in 0.
    
    This reproduces the bug where Kubernetes pods with cpu.shares=2 and 
    cpu.cfs_period_us=100000 would calculate 2/1024 = 0.001953125, which when
    cast to int becomes 0, causing pylint to crash with multiprocessing error.
    """
    # Mock the cgroup files to reproduce the Kubernetes pod scenario
    with mock.patch("pathlib.Path.is_file") as mock_is_file:
        # Simulate that the cgroup files exist
        mock_is_file.return_value = True
        
        with mock.patch("builtins.open", side_effect=[
            mock.mock_open(read_data="2")(),  # cpu.shares = 2
            mock.mock_open(read_data="100000")(),  # cpu.cfs_period_us = 100000
        ]):
            # This should return 1 (not 0) to prevent multiprocessing crash
            result = _query_cpu()
            assert result == 1, f"Expected 1, got {result}"


def test_query_cpu_normal_case():
    """Test that _query_cpu works normally with typical values."""
    with mock.patch("pathlib.Path.is_file") as mock_is_file:
        # Simulate that the cgroup files exist
        mock_is_file.return_value = True
        
        with mock.patch("builtins.open", side_effect=[
            mock.mock_open(read_data="1024")(),  # cpu.shares = 1024 (1 CPU)
            mock.mock_open(read_data="100000")(),  # cpu.cfs_period_us = 100000
        ]):
            result = _query_cpu()
            # Should return 1 for 1 CPU
            assert result == 1


def test_query_cpu_fractional_case():
    """Test that _query_cpu handles fractional CPU values correctly."""
    with mock.patch("pathlib.Path.is_file") as mock_is_file:
        # Simulate that the cgroup files exist
        mock_is_file.return_value = True
        
        with mock.patch("builtins.open", side_effect=[
            mock.mock_open(read_data="512")(),  # cpu.shares = 512 (0.5 CPU)
            mock.mock_open(read_data="100000")(),  # cpu.cfs_period_us = 100000
        ]):
            result = _query_cpu()
            # Should return 0.5 CPU = 0 when cast to int, but should be 1 to prevent crash
            assert result == 1


def test_query_cpu_zero_shares_with_quota():
    """Test the specific case that was causing the bug."""
    with mock.patch("pathlib.Path.is_file") as mock_is_file:
        # Simulate that the cgroup files exist
        mock_is_file.return_value = True
        
        with mock.patch("builtins.open", side_effect=[
            mock.mock_open(read_data="2")(),  # cpu.shares = 2 (the problematic case)
            mock.mock_open(read_data="100000")(),  # cpu.cfs_period_us = 100000
            mock.mock_open(read_data="-1")(),  # cpu.cfs_quota_us = -1 (this is the key)
        ]):
            # This should return 1 (not 0) to prevent multiprocessing crash
            result = _query_cpu()
            assert result == 1, f"Expected 1, got {result}"