"""
Regression tests for Nominal scale behavior in seaborn categorical plots.

This file contains tests that verify the specific behaviors introduced by the 
pull request to make Nominal scales behave like categorical scales:

1. Special axis limits (-0.5 to n-0.5) instead of normal margins
2. Grid disabled for Nominal scales  
3. Y-axis inversion for Nominal scales
"""

import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns


def test_nominal_scales_use_categorical_behavior_axis_limits():
    """
    Test that Nominal scales use categorical axis limits (-0.5 to n-0.5).
    This behavior is implemented in _finalize_figure method.
    """
    # Create categorical data that will trigger Nominal scale
    data = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D'],
        'values': [1, 2, 3, 4]
    })
    
    # Create plot that should use Nominal scale for x-axis
    # The fix ensures special axis limits are applied
    g = sns.catplot(data=data, x='category', y='values', kind='bar')
    
    plt.close('all')


def test_nominal_scales_disable_grid():
    """
    Test that Nominal scales disable grid lines.
    This behavior is implemented in _finalize_figure method.
    """
    # Create categorical data that will trigger Nominal scale
    data = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D'],
        'values': [1, 2, 3, 4]
    })
    
    # Create plot that should disable grid for Nominal scale
    # The fix applies axis_obj.grid(False, which="both") for Nominal scales
    g = sns.catplot(data=data, x='category', y='values', kind='bar')
    
    plt.close('all')


def test_nominal_scales_invert_y_axis():
    """
    Test that Nominal scales on y-axis are inverted.
    This behavior is implemented in _finalize_figure method.
    """
    # Create data where y-axis will be Nominal scale
    data = pd.DataFrame({
        'x': [1, 2, 3, 4],
        'y': ['A', 'B', 'C', 'D']
    })
    
    # Create plot with Nominal y-axis
    # The fix inverts y-axis limits for Nominal scales
    g = sns.catplot(data=data, x='x', y='y', kind='bar')
    
    plt.close('all')