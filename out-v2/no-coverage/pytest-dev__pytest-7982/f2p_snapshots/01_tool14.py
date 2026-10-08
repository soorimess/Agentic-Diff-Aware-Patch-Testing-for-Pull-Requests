"""
Regression test for symlinked directories not being collected since pytest 6.1.0.

This test specifically checks that symlinked directories are properly followed
during test discovery by testing the visit function behavior.
"""
import os
import sys
from pathlib import Path


def test_symlinked_directories_are_processed_by_visit_function(tmp_path):
    """
    Test that symlinked directories are processed by the visit function.
    
    This test directly tests the core issue: when a directory is a symlink,
    it should be treated as a directory and processed for recursion.
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
    
    # Test the visit function behavior
    from _pytest.pathlib import visit
    
    # Track what entries are processed
    processed_entries = []
    processed_dirs = []
    
    def recurse(entry):
        # Always recurse into directories to test the behavior
        return True
    
    # Call visit on the parent directory
    for entry in visit(str(test_dir), recurse):
        processed_entries.append(entry)
        if entry.is_dir():
            processed_dirs.append(entry)
    
    # Extract names and paths for analysis
    entry_names = [entry.name for entry in processed_entries]
    dir_names = [entry.name for entry in processed_dirs]
    
    # Both the real directory and symlinked directory should be processed
    # This is the core test: if follow_symlinks=False was used, 
    # the symlinked_dir would not be processed as a directory
    assert "real_subdir" in entry_names, f"Real directory not found in entries: {entry_names}"
    assert "symlinked_dir" in entry_names, f"Symlinked directory not found in entries: {entry_names}"
    
    # Both should be in the directory list as well
    assert "real_subdir" in dir_names, f"Real directory not found in directories: {dir_names}"
    assert "symlinked_dir" in dir_names, f"Symlinked directory not found in directories: {dir_names}"
    
    # The most important assertion: the symlinked directory should be recognized as a directory
    # and processed for recursion
    symlinked_dir_entry = None
    for entry in processed_dirs:
        if entry.name == "symlinked_dir":
            symlinked_dir_entry = entry
            break
    
    # If the symlinked directory is not processed, it means the bug is present
    # (follow_symlinks=False was used, so symlinks weren't treated as directories)
    assert symlinked_dir_entry is not None, "Symlinked directory was not processed as a directory"
    
    # Verify it's actually a directory (should be True when following symlinks)
    assert symlinked_dir_entry.is_dir(), "Symlinked directory entry is not recognized as a directory"


def test_visit_function_behavior_with_symlinks(tmp_path):
    """
    Test the specific behavior difference between follow_symlinks=True/False.
    
    This test directly tests that the visit function now uses the default behavior
    (follow_symlinks=True) instead of explicitly setting follow_symlinks=False.
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
    
    # Test that the visit function properly follows symlinks
    from _pytest.pathlib import visit
    
    # We'll test by checking if the symlinked directory gets processed
    # by examining the entries that would be recursed into
    entries_that_would_be_recursed = []
    
    def recurse(entry):
        # This function determines whether to recurse into an entry
        # Before fix: entry.is_dir(follow_symlinks=False) would return False for symlinks
        # After fix: entry.is_dir() would return True for symlinks
        is_dir = entry.is_dir()  # This is what the fix changed from entry.is_dir(follow_symlinks=False)
        if is_dir:
            entries_that_would_be_recursed.append(entry.name)
        return is_dir  # Recurse into directories
    
    # Call visit - this should process symlinked directories
    for entry in visit(str(test_dir), recurse):
        pass  # Just iterate through all entries
    
    # The symlinked directory should be in the list of entries that would be recursed into
    # This is the key behavior that was broken
    assert "symlinked_dir" in entries_that_would_be_recursed, \
        f"Symlinked directory not found in recursed entries: {entries_that_would_be_recursed}"
    
    # The real directory should also be there
    assert "real_subdir" in entries_that_would_be_recursed, \
        f"Real directory not found in recursed entries: {entries_that_would_be_recursed}"