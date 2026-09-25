"""
Regression test for Nominal scale behavior fix in seaborn.

The fix for Nominal scales in seaborn categorical plots should:
1. Use categorical-style limits (-0.5 to nticks-0.5) instead of standard margins
2. Disable grid lines for Nominal scales despite matplotlib styling
3. Invert y-axis limits when Nominal scale is on y-axis

This test ensures that when Nominal scales are used, they get the special categorical behavior.
"""
import matplotlib.pyplot as plt
import pandas as pd
import pytest

import seaborn as sns


def test_nominal_scale_uses_categorical_limits():
    """
    Test that Nominal scales use -0.5 to nticks-0.5 limits instead of standard margins.
    Before fix: limits are standard matplotlib margins like (-0.15, 3.15) 
    After fix: limits should be (-0.5, 3.5) for 4 categories
    """
    # Create data with 4 categories to make the behavior clear 
    data = pd.DataFrame({
        'x': ['A', 'B', 'C', 'D'], 
        'y': [1, 2, 3, 4]
    })
    
    # Create plot - x-axis will use Nominal scale (based on string values)
    p = sns.scatterplot(data=data, x='x', y='y')
    ax = p.axes
    
    # Get x-axis limits 
    x_limits = ax.get_xlim()
    print(f"X-axis limits with Nominal scale: {x_limits}")
    
    # The fix adds a block in _finalize_figure that when axis_key not in p._limits:
    # - sets limits to -0.5 to nticks-0.5 
    # - where nticks = number of ticks (4 for our data)
    # So we expect: lo=-0.5, hi=3.5
    # 
    # This assertion will fail in current (buggy) version because:
    # Current version uses standard matplotlib margin calculation which gives ~(-0.15, 3.15)
    # Fix version should produce ~(-0.5, 3.5)
    assert x_limits[0] <= -0.49, f"Expected x-limits to start at ~-0.5 for Nominal scale, got {x_limits[0]}"
    
    plt.close()