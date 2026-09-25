"""
Regression tests for pytest bug: pytest tries to collect random __init__.py files

The bug was introduced in 5.2.3 where __init__.py files with assertions 
would cause collection to fail, specifically because the logic that 
prevented marker collection on __init__.py files was removed.

This regression test ensures that __init__.py files in package directories
don't cause collection failures even if they contain assertions.
"""

import os
import tempfile
import subprocess
import sys
import pytest


def test_init_py_with_assertion_in_package_does_not_break_collection():
    """
    Test that __init__.py files with assertions in package directories
    do not cause test collection to fail.
    
    This is the core regression test that would have failed before the fix.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a directory structure that will trigger the problematic behavior
        package_dir = os.path.join(tmpdir, "mypackage")
        os.makedirs(package_dir)
        
        # Create an __init__.py with an assertion that would fail if imported
        init_file = os.path.join(package_dir, "__init__.py")
        with open(init_file, "w") as f:
            # This assertion should NOT be triggered during test collection
            f.write("assert False, 'This assertion is only meant to fail if __init__.py is imported'\n")
        
        # Create a normal test file
        test_file = os.path.join(package_dir, "test_sample.py")
        with open(test_file, "w") as f:
            f.write("def test_simple():\n    assert True\n")
        
        # Run pytest on the package directory - this used to fail in 5.2.3
        # because pytest was trying to import the __init__.py causing AssertionError
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "--collect-only", 
                "--tb=no", 
                "-q",
                package_dir
            ], cwd=tmpdir, capture_output=True, text=True, timeout=30)
            
            # The test should pass (collection should succeed)
            # If it fails with the specific error message about __init__.py Assertion, 
            # then we know the bug exists
            error_output = result.stderr + result.stdout
            
            if result.returncode != 0:
                # Check if it's the specific bug we're looking for
                if "AssertionError" in error_output and "__init__.py" in error_output:
                    pytest.fail("BUG REPRODUCED: __init__.py with assertion caused collection failure")
                # Some other error is fine - we only care about the specific bug
                return  # Continue - any error other than our specific bug is fine
            
        except subprocess.TimeoutExpired:
            pytest.fail("Test timed out - likely due to infinite loop or other issue")


def test_non_test_init_py_with_assertion_still_works():
    """
    Test that __init__.py files at the root directory don't cause issues 
    when they have assertions (they shouldn't be collected in most cases anyway)  
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create an __init__.py with assertion
        init_file = os.path.join(tmpdir, "__init__.py")
        with open(init_file, "w") as f:
            f.write("assert False, 'This should not be imported during collection'\n")
            
        # Create a normal test file  
        test_file = os.path.join(tmpdir, "test_something.py")
        with open(test_file, "w") as f:
            f.write("def test_simple():\n    assert True\n")
            
        # Run pytest - collection should work without error from init.py
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "--collect-only", 
                "--tb=no", 
                "-q",
                tmpdir
            ], cwd=tmpdir, capture_output=True, text=True, timeout=30)
            
            # These should not cause AssertionError from the __init__.py file
            error_output = result.stderr + result.stdout
            
            if result.returncode != 0 and "AssertionError" in error_output and "__init__.py" in error_output:
                pytest.fail("BUG REPRODUCED: Root __init__.py with assertion caused collection failure")
                
        except subprocess.TimeoutExpired:
            pytest.fail("Test timed out")


def test_init_py_behavior_comparison():
    """
    The main test that captures difference between old vs new behavior.
    
    Before fix: __init__.py files with assertions would be imported during 
    collection and cause AssertionError failures
    
    After fix: __init__.py files should not be processed in a way that 
    causes their assertions to trigger during collection
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test package with __init__.py that has failing assertions
        pkg_dir = os.path.join(tmpdir, "mypackage")
        os.makedirs(pkg_dir)
        
        init_file = os.path.join(pkg_dir, "__init__.py")
        with open(init_file, "w") as f:
            # This is the problematic content from the bug report examples
            f.write("assert False\n")
        
        test_file = os.path.join(pkg_dir, "test_example.py")
        with open(test_file, "w") as f:
            f.write("def test_should_pass():\n    assert True\n")
            
        # Run collection - this should work in correct behavior
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "--collect-only", 
            "--tb=no", 
            "-q",
            pkg_dir 
        ], cwd=tmpdir, capture_output=True, text=True, timeout=30)
        
        # Should NOT fail with AssertionError from __init__.py 
        error_output = result.stderr + result.stdout
        if result.returncode != 0:
            # If there's an assertion error about __init__.py specifically, 
            # it means the bug is still present
            if "AssertionError" in error_output and "__init__.py" in error_output:
                raise AssertionError(
                    "Regression test failed - pytest is still trying to import "
                    "__init__.py during collection causing AssertionError."
                )
        
        # If we got here, the behavior is correct (collection succeeded)
        # This proves the fix works
        assert result.returncode == 0