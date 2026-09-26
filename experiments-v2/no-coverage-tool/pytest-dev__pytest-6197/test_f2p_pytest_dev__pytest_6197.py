"""
Regression test for pytest issue where __init__.py files are incorrectly collected
and imported during test collection, causing failures when __init__.py contains
code that would fail during import.

This tests the regression in pytest 5.2.3 where __init__.py files were being 
imported during collection, causing assertion errors and import errors.
"""
import os
import pytest


def test_init_py_with_assertion_error_not_imported_during_collection(testdir):
    """Test that __init__.py files with assertion errors are not imported during collection."""
    # Create a directory structure that would cause import issues
    testdir.tmpdir.join("problematic_package").mkdir()
    init_file = testdir.tmpdir.join("problematic_package").join("__init__.py")
    init_file.write("assert False  # This should not be imported during collection")
    
    # Create a valid test file
    testdir.makepyfile(
        test_normal="""
        def test_something():
            assert True
        """
    )
    
    # Run pytest - it should not fail due to __init__.py import
    # In the buggy version, this would fail with AssertionError
    result = testdir.runpytest("-v", "--collect-only")
    
    # The collection should succeed (not fail due to __init__.py import)
    # This means __init__.py was not imported during collection
    assert result.ret == 0


def test_init_py_with_import_error_not_imported_during_collection(testdir):
    """Test that __init__.py files with import errors are not imported during collection."""
    # Create a directory structure that would cause import issues
    testdir.tmpdir.join("bad_package").mkdir()
    init_file = testdir.tmpdir.join("bad_package").join("__init__.py")
    init_file.write("import non_existent_module  # This should not be imported during collection")
    
    # Create a valid test file
    testdir.makepyfile(
        test_normal="""
        def test_something():
            assert True
        """
    )
    
    # Run pytest - it should not fail due to __init__.py import
    # In the buggy version, this would fail with ImportError
    result = testdir.runpytest("-v", "--collect-only")
    
    # The collection should succeed (not fail due to __init__.py import)
    # This means __init__.py was not imported during collection
    assert result.ret == 0


def test_normal_init_py_with_valid_code_still_works(testdir):
    """Test that __init__.py files with valid code still work normally."""
    # Create a directory with a valid __init__.py that defines test functions
    testdir.tmpdir.join("valid_package").mkdir()
    init_file = testdir.tmpdir.join("valid_package").join("__init__.py")
    init_file.write("def test_from_init():\n    assert True")
    
    # Create a valid test file
    testdir.makepyfile(
        test_normal="""
        def test_something():
            assert True
        """
    )
    
    # Run pytest - it should work normally
    result = testdir.runpytest("-v")
    
    # Should pass without issues
    assert result.ret == 0