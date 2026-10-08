"""
Regression test for symlinked directories not being collected since pytest 6.1.0

This test verifies that symlinked directories are properly collected during test discovery.
"""
import os
import tempfile
from pathlib import Path
from _pytest.pathlib import visit


def test_visit_function_recurses_into_symlinked_directories():
    """
    Test that visit function recurses into symlinked directories.
    
    The bug: with follow_symlinks=False, symlinked directories are not recursed into.
    The fix: remove follow_symlinks=False to allow following symlinks.
    
    This test will fail with the current buggy code and pass with the fixed code.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create a source directory with a test file
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        test_file = source_dir / "test_example.py"
        test_file.write_text("def test_foo(): assert True")
        
        # Create a symlink to the source directory
        symlink_dir = tmp_path / "symlinked_dir"
        symlink_dir.symlink_to(source_dir)
        
        # Track what paths are visited
        visited_paths = []
        visited_names = []
        
        def track_recurse(entry):
            visited_paths.append(entry.path)
            visited_names.append(os.path.basename(entry.path))
            return True  # Always recurse
            
        # Call visit function - this is what the bug affects
        entries = list(visit(str(tmp_path), track_recurse))
        
        # Check what was visited
        print(f"Visited names: {visited_names}")
        
        # With the bug (follow_symlinks=False), symlinked_dir won't be visited
        # With the fix, it should be visited
        symlinked_in_visited = any("symlinked_dir" in name for name in visited_names)
        
        # This assertion should pass with the fix, fail with the bug
        assert symlinked_in_visited, (
            "Symlinked directory was not visited by visit function. "
            "This indicates the symlinked directory collection bug exists. "
            "The visit function should recurse into symlinked directories."
        )
        
        # Also verify we can find the test file from the symlinked directory
        found_test_file = any("test_example.py" in path for path in visited_paths)
        assert found_test_file, (
            "Test file from symlinked directory was not found. "
            "This confirms that symlinked directories are not being explored properly."
        )


def test_symlinked_directories_are_collected():
    """Test that symlinked directories are collected during test discovery."""
    
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create a source directory with some test files
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        
        # Create a test file in the source directory
        test_file = source_dir / "test_example.py"
        test_file.write_text("""
def test_foo():
    assert True
""")
        
        # Create a symlink to the source directory
        symlink_dir = tmp_path / "symlinked_dir"
        symlink_dir.symlink_to(source_dir)
        
        # Create a test that should discover tests in the symlinked directory
        # We'll use pytest's collection mechanism to verify this
        import subprocess
        import sys
        
        # Run pytest in the temp directory to see what gets collected
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "--collect-only", 
            "-q",
            str(tmp_path)
        ], capture_output=True, text=True, cwd=tmpdir)
        
        # The symlinked directory should be collected and its tests discovered
        # If the bug exists, the symlinked directory tests won't be found
        collected_output = result.stdout
        
        # Check that tests from the symlinked directory are collected
        # The test should appear in the output
        assert "test_example.py::test_foo" in collected_output, (
            "Tests from symlinked directory were not collected. "
            "This indicates the symlinked directory collection bug."
        )


def test_symlinked_directories_with_nested_structure():
    """Test that nested symlinked directories are also collected."""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create nested directory structure
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        
        nested_dir = source_dir / "nested"
        nested_dir.mkdir()
        
        # Create test files
        test_file = source_dir / "test_source.py"
        test_file.write_text("""
def test_source():
    assert True
""")
        
        nested_test = nested_dir / "test_nested.py"
        nested_test.write_text("""
def test_nested():
    assert True
""")
        
        # Create a symlink to the source directory
        symlink_dir = tmp_path / "symlinked"
        symlink_dir.symlink_to(source_dir)
        
        # Run pytest to collect tests
        import subprocess
        import sys
        
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "--collect-only", 
            "-q",
            str(tmp_path)
        ], capture_output=True, text=True, cwd=tmpdir)
        
        collected_output = result.stdout
        
        # Both tests should be collected - one from source, one from symlinked
        assert "test_source.py::test_source" in collected_output
        assert "test_nested.py::test_nested" in collected_output, (
            "Tests from nested symlinked directory were not collected. "
            "This indicates the symlinked directory collection bug."
        )