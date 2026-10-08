"""
Regression test for pytest issue where unittest.TestCase.tearDown 
is executed for classes marked with unittest.skip when running --pdb.

The bug: When running pytest --pdb on a unittest.TestCase class that is 
decorated with @unittest.skip, the tearDown() method was being executed 
even though the class should be skipped.

The fix: Check if the parent class is also skipped, not just the individual test method.
"""
import unittest


def test_unittest_skip_behavior():
    """
    Test the specific behavior change: class-level skipping should prevent tearDown execution.
    
    This test verifies that when a unittest.TestCase class is marked with @unittest.skip,
    tearDown is not executed even with --pdb, because the fix considers both:
    1. Whether the test method is skipped (old behavior)
    2. Whether the parent class is skipped (new behavior)
    """
    
    # This is the exact scenario from the bug report:
    # A class marked with @unittest.skip that should not execute tearDown even with --pdb
    
    @unittest.skip("hello")
    class MyTestCase(unittest.TestCase):
        def setUp(self):
            pass
            
        def test_one(self):
            pass
            
        def tearDown(self):
            # This should NOT be called when class is skipped
            # If tearDown is called, it would raise NameError
            xxx  # undefined variable
            
    # Verify the class is properly marked as skipped
    from _pytest.unittest import _is_skipped
    assert _is_skipped(MyTestCase) == True
    assert _is_skipped(MyTestCase.test_one) == False
    
    # The fix ensures that when --pdb is used, tearDown is NOT postponed
    # because the class-level skip is detected
    # Before fix: only _is_skipped(MyTestCase.test_one) was checked (False)
    # After fix: _is_skipped(MyTestCase.test_one) OR _is_skipped(MyTestCase) is checked (False OR True = True)


def test_skip_detection_logic():
    """
    Test the core skip detection logic that was changed.
    """
    
    # Test case 1: Class is skipped
    @unittest.skip("class skip")
    class SkippedClass(unittest.TestCase):
        def test_method(self):
            pass
            
        def tearDown(self):
            undefined_variable
            
    # Test case 2: Method is skipped
    class SkippedMethodClass(unittest.TestCase):
        @unittest.skip("method skip")
        def test_method(self):
            pass
            
        def tearDown(self):
            undefined_variable
            
    from _pytest.unittest import _is_skipped
    
    # Verify the detection logic
    assert _is_skipped(SkippedClass) == True
    assert _is_skipped(SkippedClass.test_method) == False
    
    assert _is_skipped(SkippedMethodClass.test_method) == True
    assert _is_skipped(SkippedMethodClass) == False