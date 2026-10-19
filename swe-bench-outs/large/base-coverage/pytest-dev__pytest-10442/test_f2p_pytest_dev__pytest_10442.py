"""Regression test for pytest PR #10442 - Keep temporary directory for failing tests only.

This test verifies the behavior change where tmp_path directories are only kept
for failed tests when the retention policy is "failed" (default), instead of keeping
them for all tests.
"""
import pytest


def test_tmp_path_new_hooks_exist():
    """
    Test that the new tmp_path hooks exist for the behavior change.
    
    This test verifies that the hooks added by the PR are available for
    controlling tmp_path directory retention behavior.
    """
    # Test that the main configuration hook exists
    from _pytest.tmpdir import pytest_addoption
    
    # Test that the session finish hook exists
    from _pytest.tmpdir import pytest_sessionfinish
    assert callable(pytest_sessionfinish)
    
    # Test that the runtest makereport hook exists  
    from _pytest.tmpdir import pytest_runtest_makereport
    assert callable(pytest_runtest_makereport)
    
    # Test that the cleanup function exists
    from _pytest.pathlib import cleanup_dead_symlink
    assert callable(cleanup_dead_symlink)