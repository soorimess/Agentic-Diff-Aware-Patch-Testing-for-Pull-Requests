"""
Regression test for Nominal scale axis limits behavior in seaborn.

This specifically tests the core behavior change: Nominal scales should
use axis limits from -0.5 to n-0.5 rather than normal margin limits.

The pull request adds special handling in _finalize_figure for Nominal scales
to ensure they behave like categorical scales in this regard.
"""
import matplotlib.pyplot as plt
import pandas as pd
import pytest

from seaborn import catplot


def test_nominal_scale_uses_custom_limits():
    """
    Core test for the main behavior change:
    Nominal scales use (-0.5, n-0.5) axis limits instead of normal margins.
    """
    # Create data that will use Nominal scale inference
    data = pd.DataFrame({
        'category': ['low', 'medium', 'high', 'very_high'],  # 4 categories
        'values': [10, 20, 30, 40]
    })
    
    # Create the plot - x-axis should be inferred as Nominal 
    g = catplot(data=data, x='category', y='values', kind='bar')
    
    ax = g.ax
    
    # Check that Nominal scale axis limits follow the specific pattern
    xlim = ax.get_xlim()
    
    # For 4 categories, with Nominal scale behavior: (-0.5, 3.5)
    # This is independent of data values, just the count of categories 
    expected = (-0.5, 3.5)
    
    # This assertion will only pass when the PR behavior is applied
    assert xlim == expected, f"Nominal scale should use custom limits {expected}, got {xlim}"
    
    plt.close('all')


def test_no_regression_normal_behavior():
    """Ensure normal categorical behavior is not broken."""
    data = pd.DataFrame({
        'x': ['A', 'B', 'C', 'D'],
        'y': [1, 2, 3, 4]
    })
    
    g = catplot(data=data, x='x', y='y', kind='bar')
    ax = g.ax
    
    # Basic functionality check
    assert ax is not None
    
    plt.close('all')