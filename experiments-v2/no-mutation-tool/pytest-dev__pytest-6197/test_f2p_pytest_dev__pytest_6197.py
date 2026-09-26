"""
Regression test for pytest issue where pytest 5.2.3 tries to import 
random __init__.py files during collection.

This test ensures that __init__.py files that are not part of test discovery
should not be imported during collection, even if they contain failing assertions.
"""
import pytest


def test_init_py_with_failing_assertion_does_not_break_collection(testdir):
    """
    Test that __init__.py files with failing assertions don't break collection.
    
    In pytest 5.2.3, this would cause a collection error because pytest
    tries to import ALL __init__.py files during collection, including
    those that are not test modules.
    
    The bug occurs when there's a directory with an __init__.py that has failing 
    assertions, and pytest tries to collect it during test discovery.
    """
    # Create a directory structure like:
    # test_dir/
    #   test_something.py
    #   foobar/
    #     __init__.py  <- this has failing assertion
    # The foobar directory is NOT a test directory (no test files in it)
    test_dir = testdir.tmpdir.mkdir("test_dir")
    
    # Create a regular test file that should pass collection
    test_file = test_dir.join("test_something.py")
    test_file.write("def test_pass():\n    assert True\n")
    
    # Create a subdirectory with failing __init__.py (this should NOT be treated as test module)
    sub_dir = test_dir.mkdir("foobar")
    init_file = sub_dir.join("__init__.py")
    init_file.write("assert False\n")
    
    # Collection should succeed - the __init__.py should not be imported
    # during collection since it's not a test module itself
    result = testdir.runpytest(str(test_dir), "--collect-only", "-v")
    
    # Collection should succeed (exit code 0)
    # The __init__.py with failing assertion should be ignored during collection
    assert result.ret == 0, f"Collection failed with error: {result.stdout.lines + result.stderr.lines}"