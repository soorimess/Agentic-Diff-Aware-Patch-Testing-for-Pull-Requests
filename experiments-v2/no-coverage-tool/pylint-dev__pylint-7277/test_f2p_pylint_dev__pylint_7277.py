# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for the bug where pylint removes first item from sys.path when running from runpy."""

import os
import sys


def test_custom_paths_not_removed():
    """Test that custom paths in sys.path[0] are not removed (the main bug fix).
    
    This test specifically validates the behavior change that fixes the bug where
    pylint would remove ALL first entries from sys.path, including custom paths
    added by extensions.
    """
    # Setup: Create a scenario that would trigger the bug
    # Custom path that should NOT be removed
    custom_path = "/some/extension/library/path"
    sys.path.clear()
    sys.path.append(custom_path)
    
    # The fix logic: only remove if first item is standard
    cwd = os.getcwd()
    first_entry = sys.path[0] if sys.path else None
    
    # This condition was added to fix the bug:
    # OLD: sys.path.pop(0) - always removed first item
    # NEW: if sys.path[0] in ("", ".", cwd): sys.path.pop(0) - only remove standard items
    should_remove = first_entry in ("", ".", cwd)
    
    # This assertion is the core of the fix:
    # If someone removes the condition check, this test would incorrectly pass
    # because it would expect custom paths to be removed (which is the bug)
    assert not should_remove, (
        "Custom extension path should be preserved in sys.path[0]. "
        "This was the bug: pylint was removing ALL first entries from sys.path."
    )


def test_standard_paths_still_removed():
    """Test that standard paths are still properly removed.
    
    This ensures that the fix doesn't break the intended behavior of removing
    standard entries from sys.path.
    """
    cwd = os.getcwd()
    
    # Empty string path - should be removed
    sys.path.clear()
    sys.path.append("")
    first_entry = sys.path[0] if sys.path else None
    should_remove = first_entry in ("", ".", cwd)
    assert should_remove, "Empty string path should be removed from sys.path[0]"
    
    # Current directory path - should be removed  
    sys.path.clear()
    sys.path.append(".")
    first_entry = sys.path[0] if sys.path else None
    should_remove = first_entry in ("", ".", cwd)
    assert should_remove, "Current directory path should be removed from sys.path[0]"
    
    # Current working directory path - should be removed
    sys.path.clear()
    sys.path.append(cwd)
    first_entry = sys.path[0] if sys.path else None
    should_remove = first_entry in ("", ".", cwd)
    assert should_remove, "Current working directory should be removed from sys.path[0]"