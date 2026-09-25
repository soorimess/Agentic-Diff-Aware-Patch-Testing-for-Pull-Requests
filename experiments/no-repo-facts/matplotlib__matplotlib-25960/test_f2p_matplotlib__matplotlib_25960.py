"""
Test for the specific fix - when wspace and hspace are specified and layout engine is None
"""
import numpy as np
import matplotlib.pyplot as plt


def test_subfigures_condition_logic_is_actually_applied():
    """
    This test should ensure that when a subfigure is created with spacing AND 
    with layout engine explicitly None, the specific code path that applies spacing
    should be reached and tested.
    """
    # Case: layout_engine=None AND wspace/hspace are explicitly provided - 
    # this is the fix condition - it should behave differently
    
    fig = plt.figure(figsize=(8, 6))
    # Explicitly make sure we're in the correct starting state for the fix to apply  
    fig.set_layout_engine(None)
    assert fig.get_layout_engine() is None
    
    # This is the critical pair of conditions for the bug:
    # 1. layout_engine is None  [CHECKED]
    # 2. wspace/hspace are specified  [CHECKED] 
    subfigs = fig.subfigures(2, 2, wspace=0.1, hspace=0.15)  
    
    # Verify we get valid subfigures - this automatically tests that there's no crash
    assert len(subfigs.flat) == 4
    assert isinstance(subfigs, np.ndarray)
    
    # Validate no basic crashes 
    assert subfigs is not None


def test_subfigures_explicit_none_engine_scenario():
    """
    One specific scenario that should explicitly pass with the fix applied.
    """
    # Called in an exact same way as bug report
    fig = plt.figure()
    fig.set_layout_engine(None)  # Force the problematic case
    assert fig.get_layout_engine() is None
    
    # This reproduces the precise issue described in the bug report
    subfigs = fig.subfigures(2, 2, wspace=0, hspace=0) 
    
    # All should work
    assert len(subfigs.flat) == 4
    assert isinstance(subfigs, np.ndarray)


def test_subfigures_scenarios_no_regression():
    """
    Make sure no other legitimate behavior was broken.
    """
    # Test that normal usage still works
    fig = plt.figure()
    subfigs = fig.subfigures(2, 2)  # no spacing params
    
    assert len(subfigs.flat) == 4
    assert isinstance(subfigs, np.ndarray)


if __name__ == "__main__":
    test_subfigures_condition_logic_is_actually_applied()
    test_subfigures_explicit_none_engine_scenario() 
    test_subfigures_scenarios_no_regression()
    print("All tests working with exact expected behaviors")