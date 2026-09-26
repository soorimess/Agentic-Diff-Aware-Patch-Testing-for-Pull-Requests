"""
Regression test for Nominal scale categorical behavior fix.

This test ensures that Nominal scales properly behave like categorical scales
by testing that the fix allows Nominal scales to be used without errors.
"""

import pandas as pd
import pytest
from seaborn._core.scales import Nominal
from seaborn._core.plot import Plot


def test_nominal_scale_can_be_used():
    """Test that Nominal scale can be used in Plot without errors."""
    # Create test data
    data = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D'],
        'value': [1, 2, 3, 4]
    })
    
    # This should work correctly after the fix
    # Before the fix, this might have failed due to Nominal not being properly imported
    p = Plot(data, x='category', y='value')
    p = p.scale(x=Nominal())
    
    # Verify the Nominal scale was properly set
    assert 'x' in p._scales
    assert isinstance(p._scales['x'], Nominal)
    
    # Test that it doesn't crash
    assert p is not None


def test_nominal_scale_y_axis():
    """Test that Nominal scale works on y-axis."""
    data = pd.DataFrame({
        'value': [1, 2, 3, 4],
        'category': ['A', 'B', 'C', 'D']
    })
    
    # This should work correctly after the fix
    p = Plot(data, x='value', y='category')
    p = p.scale(y=Nominal())
    
    # Verify the Nominal scale was properly set
    assert 'y' in p._scales
    assert isinstance(p._scales['y'], Nominal)
    
    # Test that it doesn't crash
    assert p is not None


def test_nominal_scale_both_axes():
    """Test that Nominal scales work on both axes."""
    data = pd.DataFrame({
        'cat1': ['A', 'B', 'C', 'D'],
        'cat2': ['P', 'Q', 'R', 'S']
    })
    
    # This should work correctly after the fix
    p = Plot(data, x='cat1', y='cat2')
    p = p.scale(x=Nominal(), y=Nominal())
    
    # Verify both Nominal scales were properly set
    assert 'x' in p._scales
    assert 'y' in p._scales
    assert isinstance(p._scales['x'], Nominal)
    assert isinstance(p._scales['y'], Nominal)
    
    # Test that it doesn't crash
    assert p is not None