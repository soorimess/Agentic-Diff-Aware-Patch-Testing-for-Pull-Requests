import unittest
import pytest
from _pytest.pytester import Pytester


def test_skip_class_with_pdb(pytester: Pytester) -> None:
    """Test that tearDown is not called when a class is skipped with --pdb.
    
    This is a regression test for the bug where unittest.TestCase.tearDown
    was executed for classes marked with unittest.skip when running --pdb.
    """
    testfile = pytester.makepyfile(
        """
        import unittest

        @unittest.skip("hello")
        class MyTestCase(unittest.TestCase):
            def setUp(self):
                # This should not be called when the class is skipped
                raise RuntimeError("setUp should not be called for skipped class")
                
            def test_one(self):
                pass
                
            def tearDown(self):
                # This should not be called when the class is skipped
                raise RuntimeError("tearDown should not be called for skipped class")
        """
    )
    
    # Run with --pdb to trigger the bug
    result = pytester.runpytest(testfile, "--pdb", "-v")
    
    # The test should be skipped, not cause a RuntimeError from tearDown
    # If the bug exists, we'll see a NameError or RuntimeError from tearDown
    assert result.ret == 0  # Should pass (test is skipped)
    
    # Check that the test was actually skipped (not run)
    result.stdout.fnmatch_lines(["*s*MyTestCase*"])


def test_skip_class_without_pdb(pytester: Pytester) -> None:
    """Test that tearDown is not called when a class is skipped without --pdb.
    
    This should work correctly in both old and new versions.
    """
    testfile = pytester.makepyfile(
        """
        import unittest

        @unittest.skip("hello")
        class MyTestCase(unittest.TestCase):
            def setUp(self):
                # This should not be called when the class is skipped
                raise RuntimeError("setUp should not be called for skipped class")
                
            def test_one(self):
                pass
                
            def tearDown(self):
                # This should not be called when the class is skipped
                raise RuntimeError("tearDown should not be called for skipped class")
        """
    )
    
    # Run without --pdb (should work fine)
    result = pytester.runpytest(testfile, "-v")
    
    # The test should be skipped, not cause a RuntimeError from tearDown
    assert result.ret == 0  # Should pass (test is skipped)
    
    # Check that the test was actually skipped (not run)
    result.stdout.fnmatch_lines(["*s*MyTestCase*"])


def test_skip_method_with_pdb(pytester: Pytester) -> None:
    """Test that tearDown is not called when a method is skipped with --pdb.
    
    This is a control test to make sure method-level skipping works.
    """
    testfile = pytester.makepyfile(
        """
        import unittest

        class MyTestCase(unittest.TestCase):
            @unittest.skip("hello")
            def test_one(self):
                pass
                
            def tearDown(self):
                # This should not be called when the method is skipped
                raise RuntimeError("tearDown should not be called for skipped method")
        """
    )
    
    # Run with --pdb
    result = pytester.runpytest(testfile, "--pdb", "-v")
    
    # The test should be skipped, not cause a RuntimeError from tearDown
    assert result.ret == 0  # Should pass (test is skipped)
    
    # Check that the test was actually skipped (not run)
    result.stdout.fnmatch_lines(["*s*MyTestCase*"])