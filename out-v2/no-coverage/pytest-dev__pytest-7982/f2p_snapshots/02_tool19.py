"""
Regression test for symlinked directories not being collected since pytest 6.1.0.

This test specifically checks that symlinked directories are properly followed
during test discovery by testing the visit function behavior.
"""
import os
import sys
from pathlib import Path


def test_symlinked_directories_are_processed_for_recursion(tmp_path):
    """
    Test that symlinked directories are processed for recursion in the visit function.
    
    This is the core test for the bug fix: when a symlink points to a directory,
    it should be treated as a directory and recursed into.
    """
    # Create a test directory structure
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    
    # Create a subdirectory with content
    real_dir = test_dir / "real_subdir"
    real_dir.mkdir()
    
    # Create a file in the real directory
    test_file = real_dir / "test_file.py"
    test_file.write_text("def test_foo(): pass")
    
    # Create a symlink to the directory
    symlink_dir = test_dir / "symlinked_dir"
    if sys.platform == "win32":
        # On Windows, we need to create a directory junction
        os.system(f"mklink /J {symlink_dir} {real_dir}")
    else:
        # On Unix-like systems, create a symbolic link
        os.symlink(real_dir, symlink_dir)
    
    # Verify the symlink exists
    assert symlink_dir.is_symlink()
    assert symlink_dir.exists()
    
    # Test that the visit function properly follows symlinks for recursion
    from _pytest.pathlib import visit
    
    # Track which entries would be recursed into
    recursed_entries = []
    
    def recurse(entry):
        # This determines whether we recurse into an entry
        is_dir = entry.is_dir()  # This is what changed from follow_symlinks=False
        if is_dir:
            recursed_entries.append(entry.name)
        return is_dir
    
    # Call visit - this should process symlinked directories for recursion
    for entry in visit(str(test_dir), recurse):
        pass  # Just iterate through all entries
    
    # Both directories should be recursed into
    # Before the fix (follow_symlinks=False), symlinked_dir would NOT be recursed
    # After the fix (follow_symlinks=True/default), symlinked_dir SHOULD be recursed
    assert "real_subdir" in recursed_entries, f"Real directory not recursed: {recursed_entries}"
    assert "symlinked_dir" in recursed_entries, f"Symlinked directory not recursed: {recursed_entries}"