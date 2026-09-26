"""
Regression test for pytest issue where __init__.py files are imported during collection.

In pytest 5.2.3, __init__.py files under the current directory were being imported
during test collection, causing collection to fail if the __init__.py contained
code that would raise an exception.
"""
import os
import tempfile
import pytest


def test_init_py_file_not_imported_during_collection(testdir):
    """
    Test that __init__.py files are not imported during collection.
    
    This is a regression test for the bug where pytest 5.2.3 tried to import
    any __init__.py file under the current directory, causing collection to fail
    if the __init__.py contained code that would raise an exception.
    """
    # Create a problematic __init__.py that will fail on import
    testdir.makepyfile(**{
        "foobar/__init__.py": "assert False",
        "test_foo.py": "def test_pass(): assert True"
    })
    
    # This should work without errors - the __init__.py should not be imported
    # during collection because it's not a test file
    result = testdir.runpytest("-v", "--collect-only")
    
    # The collection should succeed (exit code 0) even though __init__.py has assert False
    # If it fails, that's the bug we're testing for
    assert result.ret == 0, f"Collection failed with error: {result.stderr}"


def test_init_py_file_with_assert_false(testdir):
    """
    Test that __init__.py files with assert False don't cause collection to fail.
    
    This is the exact scenario from the bug report.
    """
    # Create the exact scenario from the bug report using testdir
    testdir.makepyfile(**{
        "foobar/__init__.py": "assert False",
        "test_foo.py": "def test_pass(): assert True"
    })
    
    # Run pytest - this should succeed in 5.2.2 but fail in 5.2.3
    # (the bug is that __init__.py gets imported during collection)
    result = testdir.runpytest("-v")
    
    # In the buggy version, this would fail with AssertionError from __init__.py
    # In the fixed version, this should succeed
    assert result.ret == 0, f"Test collection failed with error: {result.stderr}"