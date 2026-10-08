"""
Regression test for symlinked directory collection issue.
Tests that symlinked directories are properly collected since pytest 6.1.0.
"""
import os
import sys
from pathlib import Path


def test_visit_function_recurses_into_symlinked_directories(tmp_path):
    """
    Test that visit function recurses into symlinked directories.
    
    This test verifies that the fix for pytest issue #7982 works correctly.
    Before the fix, symlinked directories were not being recursed into due to
    follow_symlinks=False parameter in entry.is_dir().
    """
    # Create directory structure
    original_dir = tmp_path / "original"
    original_dir.mkdir()
    
    nested_dir = original_dir / "nested"
    nested_dir.mkdir()
    
    # Create a test file in nested directory
    test_file = nested_dir / "test_file.py"
    test_file.write_text("""
def test_function():
    assert True
""")
    
    # Create symlink to nested directory
    symlink_dir = tmp_path / "symlinked"
    
    try:
        os.symlink(nested_dir, symlink_dir)
        symlink_created = True
    except (OSError, NotImplementedError):
        # Fallback for systems that don't support symlinks
        symlink_dir.mkdir()
        for item in nested_dir.iterdir():
            if item.is_file():
                (symlink_dir / item.name).write_text(item.read_text())
        symlink_created = False
    
    # Verify symlink was created
    if symlink_created:
        assert symlink_dir.is_symlink()
        assert symlink_dir.is_dir()
    
    # Import visit function
    from _pytest.pathlib import visit
    
    # Create recurse function that always returns True
    def always_recurse(entry):
        return True
    
    # Visit the symlinked directory and collect all entries
    visited_entries = []
    for entry in visit(str(symlink_dir), always_recurse):
        visited_entries.append(entry.name)
    
    # The test file should be found in visited entries
    # This demonstrates that symlinked directories are properly recursed into
    assert "test_file.py" in visited_entries, (
        "test_file.py was not found in visited entries - this indicates that "
        "symlinked directories are not being recursed into due to the bug."
    )


def test_symlinked_directories_are_collected_by_pytest(tmp_path):
    """
    Integration test showing pytest collects tests from symlinked directories.
    
    This test ensures that the pytest collection mechanism properly handles
    symlinked directories, which was broken in pytest 6.1.0.
    """
    # Create test structure like pytest would see it
    test_root = tmp_path / "test_root"
    test_root.mkdir()
    
    # Create a test directory with a test file
    test_dir = test_root / "test_suite"
    test_dir.mkdir()
    
    # Create a test file
    test_file = test_dir / "test_integration.py"
    test_file.write_text("""
def test_integration_case():
    assert True
""")
    
    # Create a symlink to the test directory
    symlink_dir = test_root / "linked_suite"
    
    try:
        os.symlink(test_dir, symlink_dir)
        symlink_created = True
    except (OSError, NotImplementedError):
        # Fallback for systems that don't support symlinks
        symlink_dir.mkdir()
        for item in test_dir.iterdir():
            if item.is_file():
                (symlink_dir / item.name).write_text(item.read_text())
        symlink_created = False
    
    if symlink_created:
        assert symlink_dir.is_symlink()
    
    # Run pytest collection on the symlinked directory
    import subprocess
    
    # Capture stdout to see what happens
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "--collect-only", 
        str(symlink_dir),
        "--quiet"
    ], capture_output=True, text=True, cwd=tmp_path)
    
    # The test should be collected from the symlinked directory
    # This is the core behavior that was broken and fixed
    assert "test_integration_case" in result.stdout, (
        "Test was not collected from symlinked directory - this demonstrates the bug "
        "where symlinked directories are not properly collected by pytest."
    )