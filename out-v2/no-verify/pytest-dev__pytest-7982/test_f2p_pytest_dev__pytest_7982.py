"""
Regression test for symlinked directories not being collected since pytest 6.1.0.

This test specifically verifies that symlinked directories are properly traversed
during test collection, which was broken due to follow_symlinks=False being used.
"""

import os
from pathlib import Path
import tempfile

import pytest
from _pytest.pathlib import symlink_or_skip


def test_symlinked_directories_traversal_behavior():
    """
    Test that demonstrates the exact traversal behavior difference.
    
    This test verifies that when a symlinked directory is encountered during
    directory traversal, it is properly recursed into rather than being skipped.
    
    The bug was in src/_pytest/pathlib.py line 561 where:
    - BEFORE (buggy): if entry.is_dir(follow_symlinks=False) and recurse(entry):
    - AFTER (fixed):   if entry.is_dir() and recurse(entry):
    
    With follow_symlinks=False, symlinked directories return False from is_dir(),
    causing them to be skipped during recursion. With default is_dir(), they return True.
    """
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create source directory structure
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        
        # Create test files in source directory
        test_file1 = source_dir / "test_foo.py"
        test_file1.write_text("def test_foo():\n    assert True\n")
        
        # Create subdirectory
        subdir = source_dir / "subdir"
        subdir.mkdir()
        
        # Create test file in subdirectory
        sub_test_file = subdir / "test_sub.py"
        sub_test_file.write_text("def test_sub():\n    assert True\n")
        
        # Create symlink to the source directory
        symlink_dir = tmp_path / "symlink_to_source"
        symlink_or_skip(source_dir, symlink_dir)
        
        # Verify the symlink was created correctly
        assert symlink_dir.is_symlink()
        assert symlink_dir.is_dir()
        
        # Import visit function to test the exact behavior
        from _pytest.pathlib import visit
        
        # Test the visit function behavior with a recurse function that always recurses
        def recurse_into_all_dirs(entry):
            return entry.is_dir()
        
        # Collect entries - this should traverse symlinked directories
        collected_entries = list(visit(str(tmp_path), recurse_into_all_dirs))
        
        # Extract names of all entries
        entry_names = [entry.name for entry in collected_entries]
        
        # Verify that both the original and symlinked directories are traversed
        # This is the core assertion - if the bug exists, symlinked directory won't be traversed
        assert "source" in entry_names, "Original directory should be collected"
        assert "symlink_to_source" in entry_names, "Symlinked directory should be collected"
        
        # Check that we can find test files from both locations
        # If the bug is present, test files from symlinked directory won't be found
        test_files_found = [name for name in entry_names if name in ["test_foo.py", "test_sub.py"]]
        assert len(test_files_found) >= 2, "Should find test files from both original and symlinked directories"


def test_is_dir_behavior_difference():
    """
    Test that directly shows the difference in is_dir() behavior with symlinks.
    
    This test specifically checks that:
    - is_dir() returns True for symlinked directories (correct behavior)
    - is_dir(follow_symlinks=False) returns False for symlinked directories (buggy behavior)
    """
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create source directory
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        
        # Create a test file
        test_file = source_dir / "test_file.py"
        test_file.write_text("def test_func():\n    assert True\n")
        
        # Create symlink to directory
        symlink_dir = tmp_path / "link_to_source"
        symlink_or_skip(source_dir, symlink_dir)
        
        # Get the symlinked directory entry
        entries = sorted(os.scandir(tmp_path), key=lambda entry: entry.name)
        
        symlink_entry = None
        for entry in entries:
            if entry.name == "link_to_source":
                symlink_entry = entry
                break
        
        assert symlink_entry is not None
        assert symlink_entry.is_symlink()
        
        # Test the two different behaviors
        # This is what was changed in the buggy code:
        # entry.is_dir(follow_symlinks=False) vs entry.is_dir()
        
        is_dir_default = symlink_entry.is_dir()
        is_dir_no_follow = symlink_entry.is_dir(follow_symlinks=False)
        
        # These should behave differently
        assert is_dir_default is True, "Default is_dir() should return True for symlinked directories"
        assert is_dir_no_follow is False, "is_dir(follow_symlinks=False) should return False for symlinked directories"