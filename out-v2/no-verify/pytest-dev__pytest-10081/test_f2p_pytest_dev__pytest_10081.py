"""
Regression test for unittest.TestCase.tearDown execution bug with --pdb.

This test ensures that when a unittest.TestCase class is marked with @unittest.skip,
its tearDown method is NOT executed even when running with --pdb.

Bug: When a unittest.TestCase class is marked with @unittest.skip,
and pytest is run with --pdb, the tearDown method was incorrectly executed.

Fix: tearDown should not be executed for skipped classes, even with --pdb.
"""

import pytest
import unittest
from _pytest.pytester import Pytester


def test_skip_class_with_pdb_does_not_call_teardown(pytester):
    """
    Test that demonstrates the bug where tearDown is called for skipped classes with --pdb.
    
    This test creates a scenario where tearDown would fail if called,
    and verifies that with --pdb it doesn't get called.
    
    Before fix: This test would fail with RuntimeError from tearDown
    After fix: This test should pass (class is skipped without calling tearDown)
    """
    # Create a test file that would fail if tearDown is called
    test_content = '''
import unittest

@unittest.skip("test skip")
class TestSkippedClass(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_something(self):
        pass
        
    def tearDown(self):
        # This should NOT be called when the class is skipped
        raise RuntimeError("tearDown should not be called for skipped class")
'''

    # Write the test file
    test_file = pytester.makepyfile(test_content)
    
    # Run with --pdb flag
    # Before the fix, this would fail with RuntimeError from tearDown
    # After the fix, this should pass (test skipped without calling tearDown)
    result = pytester.runpytest(test_file, "--pdb", "-v")
    
    # The key assertion: if tearDown was called, we'd get a RuntimeError
    # The test should pass (exit code 0) because the class is properly skipped
    # and tearDown is not executed
    assert result.ret == 0


def test_skip_class_normal_run_skips_correctly(pytester):
    """
    Test that normal run correctly skips classes (sanity check).
    """
    test_content = '''
import unittest

@unittest.skip("test skip")
class TestSkippedClass(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_something(self):
        pass
        
    def tearDown(self):
        # This should NOT be called when the class is skipped
        raise RuntimeError("tearDown should not be called for skipped class")
'''

    test_file = pytester.makepyfile(test_content)
    
    # Run normally - should skip without error
    result = pytester.runpytest(test_file, "-v")
    
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*SKIPPED*"])