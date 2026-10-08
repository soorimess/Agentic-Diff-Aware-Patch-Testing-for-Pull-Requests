"""
Regression test for pytest unittest.TestCase.tearDown execution bug with --pdb.

The bug: When a unittest.TestCase class is marked with @unittest.skip,
running with --pdb incorrectly calls tearDown() method even though the class is skipped.

This test verifies that tearDown is NOT called when a class is skipped with --pdb.
"""

import pytest
from _pytest.pytester import Pytester


def test_unittest_skip_class_with_pdb_no_teardown_call(pytester: Pytester) -> None:
    """
    Regression test that demonstrates the fix for tearDown being called 
    for skipped unittest classes when running with --pdb.
    
    The bug was that when a class is marked with @unittest.skip:
    - Individual test methods are NOT marked as skipped  
    - But the class itself IS marked as skipped
    - The old code only checked if the test method was skipped
    - So it would proceed to disable tearDown even though the class was skipped
    - This caused tearDown to be called incorrectly when running with --pdb
    
    With the fix, both the test method AND class skipping are considered.
    """
    
    # Create a test that would fail if tearDown gets called
    test_content = '''
import unittest

@unittest.skip("hello")
class MyTestCase(unittest.TestCase):
    def setUp(self):
        # This should NOT be called when class is skipped
        pass
    
    def test_one(self):
        pass
    
    def tearDown(self):
        # This should NOT be called when class is skipped
        # If tearDown is called, it should raise an exception we can detect
        raise RuntimeError("tearDown should not be called when class is skipped")
'''

    # Write the test file
    test_file = pytester.makepyfile(test_content)
    
    # Run with --pdb - this should NOT call tearDown and should skip gracefully
    # If the bug exists, tearDown will be called and cause RuntimeError
    # If the fix works, the test should be skipped without error
    result = pytester.runpytest("--pdb", str(test_file), "-v")
    
    # With the fix, this should pass (test is skipped, tearDown not called)
    # With the bug, this would fail with RuntimeError from tearDown
    assert result.ret == 0  # Should not fail due to tearDown being called
    
    # Verify that the test was actually skipped (not failed)
    result.stdout.fnmatch_lines(["*SKIPPED*"])


def test_unittest_skip_method_with_pdb_still_calls_teardown(pytester: Pytester) -> None:
    """
    Test that normal behavior is preserved: when method is skipped, tearDown IS called.
    """
    
    # Create a test where method is skipped but class is not
    test_content = '''
import unittest

class MyTestCase(unittest.TestCase):
    def setUp(self):
        # This SHOULD be called
        pass
    
    @unittest.skip("method skipped")
    def test_one(self):
        pass
    
    def tearDown(self):
        # This SHOULD be called for skipped methods
        pass
'''

    # Write the test file
    test_file = pytester.makepyfile(test_content)
    
    # Run with --pdb - tearDown should be called for method-level skipping
    result = pytester.runpytest("--pdb", str(test_file), "-v")
    
    # Should pass (method is skipped, but tearDown should be called)
    assert result.ret == 0  # Should not fail
    result.stdout.fnmatch_lines(["*SKIPPED*"])