"""
Regression test for pytest issue where __init__.py files are imported during collection
and cause failures when they contain code that raises exceptions.
"""
import pytest
import os
import tempfile
import shutil


def test_init_py_with_assertion_failure_does_not_break_collection():
    """
    Test that __init__.py files with assertion failures don't break collection.
    
    This is a regression test for pytest 5.2.3 where pytest tried to import
    any __init__.py file during collection, causing collection to fail
    if the __init__.py contained code that raises exceptions.
    """
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a package directory
        pkg_dir = os.path.join(tmpdir, "mypackage")
        os.makedirs(pkg_dir)
        
        # Create an __init__.py that will fail when imported
        init_py_path = os.path.join(pkg_dir, "__init__.py")
        with open(init_py_path, "w") as f:
            f.write("assert False, 'This should not be imported during collection'\n")
        
        # Create a regular test file
        test_file = os.path.join(tmpdir, "test_simple.py")
        with open(test_file, "w") as f:
            f.write("""
def test_something():
    assert True
""")
        
        # Try to collect tests - this should not fail even though __init__.py has an assertion error
        # We'll use pytest's testdir fixture approach
        import subprocess
        import sys
        
        # Change to the temp directory and run pytest
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "--collect-only", 
            "-q",
            str(tmpdir)
        ], cwd=tmpdir, capture_output=True, text=True)
        
        # The collection should succeed (exit code 0) even though __init__.py has an assertion error
        # If it fails, that's the bug we're testing for
        assert result.returncode == 0, f"Collection failed with error: {result.stderr}"


def test_init_py_with_syntax_error_does_not_break_collection():
    """
    Test that __init__.py files with syntax errors don't break collection.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a package directory
        pkg_dir = os.path.join(tmpdir, "mypackage")
        os.makedirs(pkg_dir)
        
        # Create an __init__.py with syntax error
        init_py_path = os.path.join(pkg_dir, "__init__.py")
        with open(init_py_path, "w") as f:
            f.write("invalid python syntax here\n")
        
        # Create a regular test file
        test_file = os.path.join(tmpdir, "test_simple.py")
        with open(test_file, "w") as f:
            f.write("""
def test_something():
    assert True
""")
        
        # Try to collect tests - this should not fail even though __init__.py has syntax error
        import subprocess
        import sys
        
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "--collect-only", 
            "-q",
            str(tmpdir)
        ], cwd=tmpdir, capture_output=True, text=True)
        
        # The collection should succeed (exit code 0) even though __init__.py has syntax error
        assert result.returncode == 0, f"Collection failed with error: {result.stderr}"


class TestInitPyCollection:
    """
    Alternative approach using pytest's testdir fixture.
    """
    
    def test_init_py_with_assertion_failure_in_package(self, testdir):
        """
        Test that __init__.py files in packages don't break collection.
        """
        # Create a package with failing __init__.py
        testdir.mkpydir("mypackage").join("__init__.py").write("assert False")
        
        # Create a test file
        testdir.makepyfile("""
            def test_something():
                assert True
        """)
        
        # Try to collect - should not fail
        result = testdir.runpytest("--collect-only", "-q")
        # This should pass (exit code 0) even though __init__.py fails
        assert result.ret == 0


    def test_init_py_with_syntax_error_in_package(self, testdir):
        """
        Test that __init__.py files with syntax errors don't break collection.
        """
        # Create a package with syntax error __init__.py
        testdir.mkpydir("mypackage").join("__init__.py").write("invalid syntax here")
        
        # Create a test file
        testdir.makepyfile("""
            def test_something():
                assert True
        """)
        
        # Try to collect - should not fail
        result = testdir.runpytest("--collect-only", "-q")
        # This should pass (exit code 0) even though __init__.py has syntax error
        assert result.ret == 0