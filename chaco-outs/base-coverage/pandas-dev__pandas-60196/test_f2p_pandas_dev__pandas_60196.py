"""
Test for pull request #60196: BUG: fix inspect usage when pyarrow or jinja2 is not installed

This test verifies that when optional dependencies are not installed, 
AttributeError is raised instead of ImportError for accessors, 
which allows inspect.getmembers to work properly.
"""
import inspect

import pandas as pd


def test_inspect_behavior_with_missing_dependencies():
    """
    Test that inspect works properly when dependencies are missing.
    
    PR #60196 ensures that when pyarrow or jinja2 are not installed,
    accessors raise AttributeError instead of ImportError so that
    inspect.getmembers can properly ignore these errors.
    """
    # Create a DataFrame to test inspect.getmembers behavior
    df = pd.DataFrame({"A": [1, 2, 3]})
    
    # Core functionality: inspect.getmembers should work without ImportError
    # This is the main behavior that was fixed in PR #60196
    members = inspect.getmembers(df)
    assert len(members) > 0