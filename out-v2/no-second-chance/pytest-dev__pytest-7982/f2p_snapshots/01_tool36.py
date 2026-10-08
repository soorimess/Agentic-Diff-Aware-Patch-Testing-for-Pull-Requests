"""
Regression test for symlinked directories not being collected since pytest 6.1.0

This test ensures that when there is a symlink to a directory in a test directory,
that symlinked directory is followed and its contents are collected as usual.
"""
import os
from pathlib import Path


def test_visit_function_follows_symlinks(tmp_path):
    """
    Test that the visit function follows symlinks correctly.
    
    This directly tests the change in behavior from:
    - entry.is_dir()  # Follows symlinks
    to:
    - entry.is_dir(follow_symlinks=False)  # Does NOT follow symlinks
    
    The visit function is used by pytest to collect tests from directories.
    """
    from _pytest.pathlib import visit
    
    # Create a directory structure with a symlink
    real_dir = tmp_path / "real"
    real_dir.mkdir()
    
    # Create a subdirectory with content
    sub_dir = real_dir / "subdir"
    sub_dir.mkdir()
    
    # Create a test file in the subdirectory
    test_file = sub_dir / "test_file.py"
    test_file.write_text("def test_func(): pass")
    
    # Create a symlink to the real directory
    symlink_dir = tmp_path / "linked"
    symlink_dir.symlink_to(real_dir)
    
    # Test that the visit function can traverse through the symlink
    visited_entries = []
    
    def recurse(entry):
        # Record that we visited this entry
        visited_entries.append(entry.name)
        # Recurse into directories - this is the key behavior
        return entry.is_dir()
    
    # Walk the directory tree
    for entry in visit(str(tmp_path), recurse):
        pass
    
    # Check that we visited entries from both the real and symlinked directories
    visited_names = visited_entries
    
    # The symlinked directory should be visited (this is the core of the fix)
    # If the bug exists (follow_symlinks=False), this assertion would fail
    assert "linked" in visited_names, "Symlinked directory should be visited"
    assert "real" in visited_names, "Real directory should be visited"
    assert "subdir" in visited_names, "Subdirectory should be accessible through symlink"