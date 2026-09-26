"""
Regression test for pytest issue where __init__.py files are imported during collection.
This test verifies that __init__.py files are not imported during collection to avoid
errors in packages that can't be imported on certain platforms.
"""
import pytest


def test_init_py_files_dont_cause_collection_errors(testdir):
    """
    Test that __init__.py files with failing code don't cause collection to fail.
    
    In version 5.2.3, pytest tried to import __init__.py files during collection,
    causing AssertionError and SyntaxError when the __init__.py contained failing code.
    This test ensures that __init__.py files are handled specially during collection.
    """
    # Create a failing __init__.py file in the test directory
    testdir.makefile(".py", __init__="assert False")
    
    # Create a regular test file
    testdir.makefile(".py", test_foo="def test_foo():\n    assert True")
    
    # Collection should succeed even though __init__.py has failing code
    # In the broken version, this fails with AssertionError from __init__.py
    # In the fixed version, this should succeed
    result = testdir.runpytest("--collect-only", "-q")
    
    # This assertion should pass after the fix is applied
    # It should fail in the current (broken) version
    assert result.ret == 0, (
        "Collection failed when it should succeed. "
        "This indicates __init__.py files are being imported during collection."
    )


def test_init_py_with_syntax_error_dont_cause_collection_errors(testdir):
    """
    Test that __init__.py files with syntax errors don't cause collection to fail.
    
    This is another aspect of the same regression - syntax errors in __init__.py 
    should not break collection.
    """
    # Create a syntax error __init__.py file in the test directory  
    testdir.makefile(".py", __init__="invalid python syntax here")
    
    # Create a regular test file
    testdir.makefile(".py", test_bar="def test_bar():\n    assert True")
    
    # Collection should succeed even though __init__.py has syntax error
    result = testdir.runpytest("--collect-only", "-q")
    
    # This assertion should pass after the fix is applied
    assert result.ret == 0, (
        "Collection failed when it should succeed due to syntax error in __init__.py. "
        "This indicates __init__.py files are being imported during collection."
    )