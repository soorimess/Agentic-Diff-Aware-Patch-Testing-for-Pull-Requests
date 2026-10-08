"""
Regression test for symlinked directories not being collected since pytest 6.1.0

This test ensures that symlinked directories are properly followed and their contents
are collected during test discovery.
"""
import os
import sys
from pathlib import Path


def test_symlinked_directory_recursion_behavior():
    """
    Test that specifically demonstrates the recursion behavior difference.
    
    The bug was that symlinked directories were not being recursed into due to
    follow_symlinks=False parameter in the condition.
    """
    from _pytest.pathlib import visit
    
    # Create a test structure that clearly shows the difference
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create a directory structure
        root = tmp_path / "root"
        root.mkdir()
        
        # Create a subdirectory with content
        subdir = root / "subdir"
        subdir.mkdir()
        
        # Create a test file in the subdirectory
        test_file = subdir / "test_file.py"
        test_file.write_text("def test_func(): pass")
        
        # Create a symlink to the subdirectory
        symlink = tmp_path / "link_to_subdir"
        os.symlink(subdir, symlink)
        
        # Track what gets processed by the recurse function
        processed_entries = []
        
        def recurse(entry):
            # Track which entries are passed to recurse function
            processed_entries.append(entry.name)
            
            # Debug information for the symlink
            if entry.name == "link_to_subdir":
                print(f"DEBUG - Recurse called on symlink:")
                print(f"  entry.name: {entry.name}")
                print(f"  entry.is_dir(): {entry.is_dir()}")
                print(f"  entry.is_dir(follow_symlinks=False): {entry.is_dir(follow_symlinks=False)}")
                print(f"  entry.is_symlink(): {entry.is_symlink()}")
            
            # Return True to recurse into directories
            return entry.is_dir()
        
        # Call visit function
        collected_entries = []
        for entry in visit(str(tmp_path), recurse):
            collected_entries.append(entry.name)
        
        print(f"Collected entries: {collected_entries}")
        print(f"Processed by recurse: {processed_entries}")
        
        # The key test: the symlink should be processed by the recurse function
        # If the bug is present, it won't be processed (recurse function won't be called)
        # If the fix is applied, it will be processed
        assert "link_to_subdir" in processed_entries, (
            "Symlinked directory was not processed by recurse function - "
            "this indicates the bug where follow_symlinks=False prevents recursion"
        )
        
        # Also check that we can find the test file from the symlinked directory
        # This ensures the symlinked directory contents are accessible
        assert "test_file.py" in collected_entries


def test_end_to_end_pytest_collection_with_symlinks():
    """
    End-to-end test that demonstrates pytest collection works with symlinked directories.
    
    This test creates a real pytest test scenario to verify the fix works in practice.
    """
    import tempfile
    import subprocess
    import sys
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create test structure
        test_root = tmp_path / "test_root"
        test_root.mkdir()
        
        # Create a real test directory
        real_dir = test_root / "real_tests"
        real_dir.mkdir()
        
        # Create a test file in the real directory
        real_test = real_dir / "test_real.py"
        real_test.write_text("""
def test_real():
    assert True
""")
        
        # Create a symlink to the test directory
        symlink_dir = test_root / "symlinked_tests"
        os.symlink(real_dir, symlink_dir)
        
        # Create a test file in the symlinked directory
        symlink_test = symlink_dir / "test_symlinked.py"
        symlink_test.write_text("""
def test_symlinked():
    assert True
""")
        
        # Run pytest to see what gets collected
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "--collect-only", 
            "-q",
            str(test_root)
        ], capture_output=True, text=True, cwd=tmpdir)
        
        collected_output = result.stdout + result.stderr
        
        print(f"Pytest collection output:\n{collected_output}")
        
        # Both tests should be collected - this is the core functionality that was broken
        assert "test_real" in collected_output
        assert "test_symlinked" in collected_output