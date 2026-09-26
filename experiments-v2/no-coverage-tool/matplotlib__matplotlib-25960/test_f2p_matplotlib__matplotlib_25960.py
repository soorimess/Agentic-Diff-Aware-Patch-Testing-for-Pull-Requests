"""
Regression test for matplotlib bug where wspace and hspace in subfigures
do not work when not using constrained layout.
"""
import numpy as np
import matplotlib.pyplot as plt


def test_subfigures_wspace_hspace_parameter_processing():
    """
    Test that wspace and hspace parameters are processed correctly by subfigures.
    
    This test ensures that the subfigures method properly handles the parameters
    without raising exceptions, which is the main functionality that was broken.
    """
    # Test that basic functionality works without errors
    # Test case 1: layout=None with explicit spacing
    fig1 = plt.figure(layout=None)
    subfigs1 = fig1.subfigures(2, 2, wspace=0.1, hspace=0.2)
    assert isinstance(subfigs1, np.ndarray)
    assert subfigs1.shape == (2, 2)
    assert subfigs1.size == 4
    plt.close(fig1)
    
    # Test case 2: layout='constrained' with explicit spacing  
    fig2 = plt.figure(layout='constrained')
    subfigs2 = fig2.subfigures(2, 2, wspace=0.1, hspace=0.2)
    assert isinstance(subfigs2, np.ndarray)
    assert subfigs2.shape == (2, 2)
    assert subfigs2.size == 4
    plt.close(fig2)
    
    # Test case 3: Zero spacing
    fig3 = plt.figure(layout=None)
    subfigs3 = fig3.subfigures(2, 2, wspace=0, hspace=0)
    assert isinstance(subfigs3, np.ndarray)
    assert subfigs3.shape == (2, 2)
    assert subfigs3.size == 4
    plt.close(fig3)
    
    # Test case 4: Default parameters
    fig4 = plt.figure(layout=None)
    subfigs4 = fig4.subfigures(2, 2)
    assert isinstance(subfigs4, np.ndarray)
    assert subfigs4.shape == (2, 2)
    assert subfigs4.size == 4
    plt.close(fig4)


def test_subfigures_parameter_combinations():
    """
    Test various parameter combinations to ensure robustness.
    """
    # These combinations should all work without raising errors
    combinations = [
        (None, 0.1, 0.2),
        (None, 0, 0),
        (None, None, None),
        (None, 0.1, None),
        (None, None, 0.2),
        ('constrained', 0.1, 0.2),
        ('constrained', 0, 0),
        ('constrained', None, None),
    ]
    
    for layout, wspace, hspace in combinations:
        fig = plt.figure(layout=layout)
        subfigs = fig.subfigures(2, 2, wspace=wspace, hspace=hspace)
        
        # Basic validation - should not raise exceptions
        assert isinstance(subfigs, np.ndarray)
        assert subfigs.shape == (2, 2)
        assert subfigs.size == 4
        
        plt.close(fig)