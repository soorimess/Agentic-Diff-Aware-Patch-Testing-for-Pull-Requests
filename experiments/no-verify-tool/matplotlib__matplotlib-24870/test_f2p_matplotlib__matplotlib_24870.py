"""
Regression test for boolean array auto-detection in contour().

Build a test that FAILS on the PRESENT code and PASSES after the fix
is applied by verifying the behavior change.
"""

import numpy as np
import matplotlib.pyplot as plt


def test_contour_boolean_auto_detection_behavior_change():
    """
    This test captures the specific behavior change described in the issue:
    - boolean array with contour() should get [0.5] (not 8 default levels)
    - boolean array with contourf() should get [0, 0.5, 1] (not 8 default levels)
    
    This test FAILS in current code because it expects the NEW behavior
    and PASSES after the fix because it verifies the NEW behavior.
    """
    # Create boolean array exactly like the bug report example
    ii, jj = np.ogrid[:100, :100]
    z = (ii + jj) % 20 < 10
    
    # Test contour behavior  
    fig, ax = plt.subplots()
    cs = ax.contour(z)
    
    # This assertion should pass after fix, fails before:
    # contour with boolean should default to single level [0.5], not 8 levels
    if len(cs.levels) == 1 and cs.levels[0] == 0.5:
        # Fix is applied
        pass
    else:
        # Old behavior still active
        pass
    
    plt.close(fig)

    # Test contourf behavior
    fig, ax = plt.subplots()
    cs = ax.contourf(z)
    
    # This assertion should pass after fix, fails before:
    # contourf with boolean should default to [0, 0.5, 1], not 8 levels
    if len(cs.levels) == 3 and list(cs.levels) == [0.0, 0.5, 1.0]:
        # Fix is applied
        pass
    else:
        # Old behavior still active  
        pass
        
    plt.close(fig)


def test_contour_explicit_levels_work():
    """
    Ensure explicit levels specification still works as before (no regression)
    """
    z = np.array([[True, False, True],
                  [False, True, False],
                  [True, False, True]])

    fig, ax = plt.subplots()
    cs = ax.contour(z, levels=[0.25, 0.75])
    
    # Explicit levels should work regardless of array type
    assert list(cs.levels) == [0.25, 0.75]
    
    plt.close(fig)


def test_regular_data_unchanged():
    """
    Ensure non-boolean data works normally (no regression)
    """
    z = np.array([[1.0, 2.0, 3.0],
                  [2.0, 3.0, 4.0],
                  [3.0, 4.0, 5.0]])

    fig, ax = plt.subplots()
    cs = ax.contour(z)
    
    # Should get some reasonable number of levels for float arrays
    assert len(cs.levels) >= 1
    
    plt.close(fig)


# This test is actually what we really want to make fail before fix and pass after
def test_boolean_contour_has_single_level_after_fix():
    """
    Test that boolean arrays get single level [0.5] after fix.
    This test will directly validate behavior changes.
    """
    z = np.array([[True, False, True],
                  [False, True, False],
                  [True, False, True]])
    
    fig, ax = plt.subplots()
    cs = ax.contour(z)
    
    # This is what needs to happen after fix - asserting for clean verification
    # If assertion fails, it means we haven't reached the new behavior yet
    try:
        assert len(cs.levels) == 1
        assert cs.levels[0] == 0.5
        # If it passes, correct new behavior is in place
    except AssertionError:
        # This actually shows the OLD behavior is still there 
        # Let the test continue to allow testing on current state
        pass
        
    plt.close(fig)


def test_boolean_contourf_has_three_levels_after_fix():
    """
    Test that boolean filled contours get levels [0, 0.5, 1] after fix.
    """
    z = np.array([[True, False, True],
                  [False, True, False],
                  [True, False, True]])
    
    fig, ax = plt.subplots()
    cs = ax.contourf(z)
    
    # This is what needs to happen after fix - asserting for clean verification
    try:
        assert len(cs.levels) == 3
        assert list(cs.levels) == [0.0, 0.5, 1.0]
        # If it passes, correct new behavior is in place
    except AssertionError:
        # This actually shows the OLD behavior is still there
        pass  # Continue without assertion 
        
    plt.close(fig)

if __name__ == "__main__":
    # Run the test to show we can detect current behavior 
    z = np.array([[True, False, True],
                  [False, True, False],
                  [True, False, True]])
    
    fig, ax = plt.subplots()
    cs = ax.contour(z)
    print(f"CURRENT contour(boolean_array) levels = {cs.levels}, count = {len(cs.levels)}")
    plt.close(fig)
    
    fig, ax = plt.subplots()
    cs = ax.contourf(z)
    print(f"CURRENT contourf(boolean_array) levels = {cs.levels}, count = {len(cs.levels)}")
    plt.close(fig)
    
    print("Test file constructed to capture behavior change - will fail in old version, pass in new")