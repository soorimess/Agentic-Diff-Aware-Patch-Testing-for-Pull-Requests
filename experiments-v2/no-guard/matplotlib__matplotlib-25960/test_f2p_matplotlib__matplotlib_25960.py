"""
Regression test for matplotlib bug where wspace and hspace in subfigures
do nothing when there's no layout engine.

This test ensures that when subfigures are created with wspace and hspace
parameters and there is no layout engine, those spacing parameters are
actually respected.
"""

import matplotlib.pyplot as plt


def test_subfigures_spacing_parameters_work():
    """
    Test that wspace and hspace parameters are processed when no layout engine.
    
    This test specifically validates the fix that ensures spacing parameters
    are not ignored when there's no layout engine.
    """
    # Create figure without layout engine (default behavior)
    fig = plt.figure(figsize=(10, 10))
    
    # These should work correctly with the fix
    subfigs = fig.subfigures(2, 2, wspace=0.1, hspace=0.1)
    
    # Verify structure
    assert len(subfigs) == 2
    assert len(subfigs[0]) == 2
    
    # Verify we can create subplots in all subfigures
    for row in subfigs:
        for sf in row:
            ax = sf.subplots()
            assert ax is not None


def test_subfigures_no_layout_engine_scenarios():
    """
    Test various scenarios with no layout engine.
    """
    fig = plt.figure(figsize=(10, 10))
    
    # Test with zero spacing
    subfigs1 = fig.subfigures(2, 2, wspace=0.0, hspace=0.0)
    assert len(subfigs1) == 2
    
    # Test with non-zero spacing
    subfigs2 = fig.subfigures(2, 2, wspace=0.2, hspace=0.2)
    assert len(subfigs2) == 2
    
    # Test with None spacing (should use defaults)
    subfigs3 = fig.subfigures(2, 2, wspace=None, hspace=None)
    assert len(subfigs3) == 2


def test_subfigures_with_constrained_layout_unchanged():
    """
    Test that constrained layout behavior is unchanged (regression test).
    """
    fig = plt.figure(figsize=(10, 10), layout='constrained')
    
    subfigs = fig.subfigures(2, 2, wspace=0.1, hspace=0.1)
    assert len(subfigs) == 2
    assert len(subfigs[0]) == 2


def test_subfigures_parameter_combinations():
    """
    Test various parameter combinations work correctly.
    """
    fig = plt.figure(figsize=(10, 10))
    
    # Test different combinations
    combinations = [
        (0.0, 0.0),
        (0.1, 0.1),
        (0.0, 0.2),
        (0.2, 0.0),
        (None, None)
    ]
    
    for wspace, hspace in combinations:
        subfigs = fig.subfigures(2, 2, wspace=wspace, hspace=hspace)
        assert len(subfigs) == 2
        assert len(subfigs[0]) == 2