"""
Regression test for symlinked directories not being collected since pytest 6.1.0

This test verifies that symlinked directories are properly followed and their
contents collected during test discovery, which was broken in pytest 6.1.0.
"""
import os
import sys
from pathlib import Path

import pytest
from _pytest.pytester import Testdir


def test_symlinked_directories_are_collected(testdir):
    """Test that symlinked directories are collected during test discovery."""
    
    # Create test directory structure
    testdir_path = Path(testdir.tmpdir)
    test_root = testdir_path / "test_root"
    test_root.mkdir()
    
    # Create a test module in root
    test_root_module = test_root / "test_root_module.py"
    test_root_module.write_text("""
def test_root():
    assert True
""")
    
    # Create a subdirectory with tests
    sub_dir = test_root / "subdir"
    sub_dir.mkdir()
    
    test_sub_module = sub_dir / "test_sub_module.py"
    test_sub_module.write_text("""
def test_sub():
    assert True
""")
    
    # Create symlink to subdirectory
    symlink_dir = test_root / "linked_subdir"
    if sys.platform != "win32":
        os.symlink(str(sub_dir), str(symlink_dir))
    else:
        # On Windows, create a copy to simulate symlink behavior
        symlink_dir.mkdir()
        for item in sub_dir.iterdir():
            if item.is_file():
                (symlink_dir / item.name).write_text(item.read_text())
            else:
                (symlink_dir / item.name).mkdir()
                for sub_item in item.iterdir():
                    (symlink_dir / item.name / sub_item.name).write_text(sub_item.read_text())
    
    # Change to the test root directory to run pytest
    old_cwd = os.getcwd()
    try:
        os.chdir(str(test_root))
        result = testdir.runpytest("--collect-only", "-q")
        output = result.stdout.str()
        
        # Both tests should be found
        # The bug: symlinked directory tests are NOT collected, only direct tests
        # So we expect to see: test_root_module.py::test_root and subdir/test_sub_module.py::test_sub
        # But if symlinked directories worked, we'd also see: linked_subdir/test_sub_module.py::test_sub
        
        assert "test_root_module.py::test_root" in output
        assert "subdir/test_sub_module.py::test_sub" in output
        
        # This is the key assertion - if symlinked directories are working properly,
        # we should see the symlinked directory path in the output
        if sys.platform != "win32":
            # On Unix systems, we expect to see the symlinked directory in the output
            # This will fail in the buggy version
            assert "linked_subdir/test_sub_module.py::test_sub" in output
        else:
            # On Windows, we can't test real symlinks, so we just check the basic functionality
            # The test should still pass because we're not testing symlink behavior on Windows
            pass
            
    finally:
        os.chdir(old_cwd)