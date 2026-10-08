"""
Regression test for pytest issue where unittest.TestCase.tearDown
is executed for classes marked with unittest.skip when running --pdb.
"""
import pytest
import unittest


def test_skip_class_with_pdb(pytester):
    """Test that tearDown is not called when a class is skipped with --pdb."""
    testfile = pytester.makepyfile("""
        import unittest

        @unittest.skip("hello")
        class MyTestCase(unittest.TestCase):
            def setUp(self):
                # This should not be called when class is skipped
                raise RuntimeError("setUp should not be called")

            def test_one(self):
                pass

            def tearDown(self):
                # This should not be called when class is skipped
                raise RuntimeError("tearDown should not be called")
    """)
    
    # Run with --pdb flag to trigger the bug
    result = pytester.runpytest("--pdb", testfile)
    
    # The test should be skipped, not fail due to tearDown being called
    result.stdout.fnmatch_lines(["*s*"])  # s indicates skipped
    assert result.ret == 0  # Should not fail


def test_skip_class_without_pdb(pytester):
    """Test that tearDown is not called when a class is skipped without --pdb."""
    testfile = pytester.makepyfile("""
        import unittest

        @unittest.skip("hello")
        class MyTestCase(unittest.TestCase):
            def setUp(self):
                # This should not be called when class is skipped
                raise RuntimeError("setUp should not be called")

            def test_one(self):
                pass

            def tearDown(self):
                # This should not be called when class is skipped
                raise RuntimeError("tearDown should not be called")
    """)
    
    # Run without --pdb flag
    result = pytester.runpytest(testfile)
    
    # The test should be skipped, not fail due to tearDown being called
    result.stdout.fnmatch_lines(["*s*"])  # s indicates skipped
    assert result.ret == 0  # Should not fail


def test_skip_test_with_pdb(pytester):
    """Test that tearDown is not called when a test is skipped with --pdb."""
    testfile = pytester.makepyfile("""
        import unittest

        class MyTestCase(unittest.TestCase):
            @unittest.skip("hello")
            def test_one(self):
                pass

            def tearDown(self):
                # This should not be called when test is skipped
                raise RuntimeError("tearDown should not be called")
    """)
    
    # Run with --pdb flag
    result = pytester.runpytest("--pdb", testfile)
    
    # The test should be skipped, not fail due to tearDown being called
    result.stdout.fnmatch_lines(["*s*"])  # s indicates skipped
    assert result.ret == 0  # Should not fail