"""
Regression test for pytest issue where tearDown() is executed for classes
marked with unittest.skip when running --pdb.
"""
import pytest
from _pytest.pytester import Pytester


def test_unittest_skip_class_with_pdb(pytester: Pytester) -> None:
    """Test that tearDown is not called when a unittest.TestCase class is skipped with --pdb."""
    testfile = pytester.makepyfile("""
        import unittest

        @unittest.skip("hello")
        class MyTestCase(unittest.TestCase):
            def setUp(self):
                pass
            def test_one(self):
                pass
            def tearDown(self):
                # This should not be called when the class is skipped
                raise RuntimeError("tearDown should not be called for skipped class")
    """)
    
    # Run with --pdb flag to trigger the bug
    result = pytester.runpytest("--pdb", testfile)
    
    # The test should be skipped, not fail due to tearDown being called
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*s*"])  # s indicates skipped


def test_unittest_skip_class_without_pdb(pytester: Pytester) -> None:
    """Test that tearDown is not called when a unittest.TestCase class is skipped without --pdb."""
    testfile = pytester.makepyfile("""
        import unittest

        @unittest.skip("hello")
        class MyTestCase(unittest.TestCase):
            def setUp(self):
                pass
            def test_one(self):
                pass
            def tearDown(self):
                # This should not be called when the class is skipped
                raise RuntimeError("tearDown should not be called for skipped class")
    """)
    
    # Run without --pdb flag
    result = pytester.runpytest(testfile)
    
    # The test should be skipped, not fail due to tearDown being called
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*s*"])  # s indicates skipped


def test_unittest_skip_class_and_method_with_pdb(pytester: Pytester) -> None:
    """
    Test that tearDown is not called when both class and individual test method are skipped.
    This tests the specific logic path that the fix addresses.
    """
    testfile = pytester.makepyfile("""
        import unittest

        @unittest.skip("class skipped")
        class MyTestCase(unittest.TestCase):
            def setUp(self):
                pass
            @unittest.skip("method skipped") 
            def test_skipped_method(self):
                pass
            def tearDown(self):
                # This should not be called when the class is skipped
                raise RuntimeError("tearDown should not be called for skipped class/method")
    """)
    
    # Run with --pdb flag
    result = pytester.runpytest("--pdb", testfile)
    
    # The test should be skipped, not fail due to tearDown being called
    assert result.ret == 0
    result.stdout.fnmatch_lines(["*s*"])  # s indicates skipped