"""
Regression test for pytest __init__.py collection bug.
"""
import pytest


def test_collection_succeeds_despite_init_py_errors(testdir):
    """
    Test that collection succeeds even when __init__.py contains import errors.
    
    This test verifies the regression where __init__.py files cause collection
    to fail in pytest 5.2.3, when they should succeed.
    """
    # Create a package with problematic __init__.py
    pkg_dir = testdir.tmpdir.mkdir("test_package")
    init_py = pkg_dir.join("__init__.py")
    init_py.write("import non_existent_module")  # This will cause import error
    
    # Add a valid test file
    test_file = pkg_dir.join("test_valid.py")
    test_file.write("def test_something(): pass")
    
    # Run pytest with collection only
    result = testdir.runpytest("--collect-only", str(pkg_dir))
    
    # With the fix applied, this should succeed (return code 0)
    # With the bug, this fails due to __init__.py import error
    assert result.ret == 0, f"Collection failed with return code {result.ret}"