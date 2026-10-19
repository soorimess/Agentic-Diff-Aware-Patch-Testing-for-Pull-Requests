"""
Regression test for matplotlib issue: function shadowing their own definition modules

This test verifies that after the fix, the fully qualified name mechanism works
properly for objects in the matplotlib.tri module.
"""

import matplotlib.tri as tri
import numpy as np


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


def test_new_trirefine_functionality():
    """
    Test that the new trirefine functionality works correctly.
    
    This test ensures that the new _trirefine.py module and its classes
    are properly accessible and functional after the fix.
    """
    # Test that UniformTriRefiner is available and can be instantiated
    assert hasattr(tri, 'UniformTriRefiner')
    assert callable(tri.UniformTriRefiner)
    
    # Test basic triangulation creation
    x = np.array([0, 1, 2, 0, 1, 2])
    y = np.array([0, 0, 0, 1, 1, 1])
    
    # Create a simple triangulation
    triangulation = tri.Triangulation(x, y)
    
    # Test that we can create a refiner
    refiner = tri.UniformTriRefiner(triangulation)
    assert refiner is not None
    assert isinstance(refiner, tri.UniformTriRefiner)


def test_triangulation_functionality():
    """
    Test that basic triangulation functionality works correctly.
    """
    # Test basic triangulation creation
    x = np.array([0, 1, 2, 0, 1, 2])
    y = np.array([0, 0, 0, 1, 1, 1])
    
    # Create a simple triangulation
    triangulation = tri.Triangulation(x, y)
    assert triangulation is not None
    assert isinstance(triangulation, tri.Triangulation)
    
    # Test that it has expected attributes
    assert hasattr(triangulation, 'x')
    assert hasattr(triangulation, 'y')
    assert hasattr(triangulation, 'triangles')


def test_trianalyzer_functionality():
    """
    Test that TriAnalyzer functionality works correctly.
    
    This tests the _tritools.py module functionality that was added.
    """
    # Test basic triangulation creation
    x = np.array([0, 1, 2, 0, 1, 2])
    y = np.array([0, 0, 0, 1, 1, 1])
    
    # Create a simple triangulation
    triangulation = tri.Triangulation(x, y)
    
    # Test that we can create a TriAnalyzer
    analyzer = tri.TriAnalyzer(triangulation)
    assert analyzer is not None
    assert isinstance(analyzer, tri.TriAnalyzer)
    
    # Test that scale_factors works
    scale_factors = analyzer.scale_factors
    assert isinstance(scale_factors, tuple)
    assert len(scale_factors) == 2
    assert all(isinstance(f, (int, float)) for f in scale_factors)
    
    # Test circle_ratios method (this exercises the _tritools.py code)
    # We'll test a simple case that should work without errors
    circle_ratios = analyzer.circle_ratios()
    # Should return a masked array or regular array
    assert circle_ratios is not None


def test_triinterpolate_functionality():
    """
    Test that basic triinterpolate functionality works correctly.
    
    This tests the _triinterpolate.py module functionality that was added.
    """
    # Test basic triangulation creation
    x = np.array([0, 1, 2, 0, 1, 2])
    y = np.array([0, 0, 0, 1, 1, 1])
    z = np.array([1, 2, 3, 4, 5, 6])
    
    # Create a simple triangulation
    triangulation = tri.Triangulation(x, y)
    
    # Test that we can create a TriInterpolator (this exercises _pseudo_inv22sym_vectorized)
    interpolator = tri.TriInterpolator(triangulation, z)
    assert interpolator is not None
    assert isinstance(interpolator, tri.TriInterpolator)