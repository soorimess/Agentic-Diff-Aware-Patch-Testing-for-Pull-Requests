"""
Regression test for matplotlib issue: function shadowing their own definition modules

This test verifies that after the fix, the fully qualified name mechanism works
properly for objects in the matplotlib.tri module.
"""

import matplotlib.tri as tri


def test_tripcolor_fully_qualified_name_approach():
    """
    Test that the fully qualified name approach works correctly.
    
    The bug report shows that the approach:
    qualname = tripcolor.__module__ + '.' + tripcolor.__name__
    obj = matplotlib
    for k in qualname.split('.')[1:]:
        obj = getattr(obj, k)
    
    Failed because of name collision between module and function.
    After the fix, this should work.
    """
    # Get the tripcolor function
    tripcolor_func = tri.tripcolor
    
    # Get the function's fully qualified name
    qualname = tripcolor_func.__module__ + '.' + tripcolor_func.__name__
    
    # This should work after the fix:
    # The qualname will be something like 'matplotlib.tri.tripcolor.tripcolor'
    # When we walk it:
    # 1. getattr(matplotlib, 'tri') -> matplotlib.tri module  
    # 2. getattr(matplotlib.tri, 'tripcolor') -> the tripcolor function
    # 3. getattr(tripcolor_function, 'tripcolor') -> should fail if there's a collision
    
    # The key insight: in the old code, there was a name collision such that
    # walking the path would fail at step 3. After the fix, it should work.
    
    # Try to walk the path
    try:
        # Split qualname and walk it
        parts = qualname.split('.')
        if len(parts) < 2:
            raise ValueError("Invalid qualname format")
            
        # Start with the root module
        obj = __import__(parts[0])  # e.g., 'matplotlib'
        
        # Walk the rest of the path
        for part in parts[1:]:  # Skip the first part (module name)
            obj = getattr(obj, part)
        
        # If we get here, we successfully walked the path
        # The final object should be the tripcolor function
        assert obj is tripcolor_func, f"Expected tripcolor function, got {type(obj)}"
        
    except AttributeError as e:
        # This is the expected failure in the old code
        # The fix should make this work
        raise AssertionError(f"Fully qualified name approach failed: {e}")
    except Exception as e:
        # Any other exception indicates a problem with the approach
        raise AssertionError(f"Unexpected error in fully qualified name approach: {e}")


def test_tripcolor_function_is_callable():
    """
    Basic test that tripcolor is still a callable function.
    """
    assert callable(tri.tripcolor)