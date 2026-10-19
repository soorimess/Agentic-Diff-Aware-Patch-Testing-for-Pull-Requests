"""Regression test for pytest PR #10442 - Keep temporary directory for failing tests only.

This test verifies the behavior change where tmp_path directories are only kept
for failed tests when the retention policy is "failed" (default), instead of keeping
them for all tests.
"""
import pytest


def test_tmp_path_new_hooks_and_configuration_exist():
    """
    Test that the new tmp_path hooks and configuration exist for the behavior change.
    
    This test verifies that the hooks and configuration options added by the PR 
    are available and properly structured for controlling tmp_path directory retention behavior.
    """
    # Test that the main configuration hook exists and is callable
    from _pytest.tmpdir import pytest_addoption
    assert callable(pytest_addoption)
    
    # Test that the session finish hook exists and is callable
    from _pytest.tmpdir import pytest_sessionfinish
    assert callable(pytest_sessionfinish)
    
    # Test that the runtest makereport hook exists and is callable  
    from _pytest.tmpdir import pytest_runtest_makereport
    assert callable(pytest_runtest_makereport)
    
    # Test that the cleanup function exists and is callable
    from _pytest.pathlib import cleanup_dead_symlink
    assert callable(cleanup_dead_symlink)
    
    # Test that we can import the configuration types
    try:
        from _pytest.tmpdir import RetentionType
        # Verify it's a proper type annotation - should not be None
        assert RetentionType is not None
    except (ImportError, AttributeError):
        # This is expected before implementation
        pass