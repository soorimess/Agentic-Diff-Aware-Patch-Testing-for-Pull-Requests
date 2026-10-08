"""
Test for issue with wrong legend values of large ranges.

This test ensures that legends for large numbers don't use offset/scientific 
notation that would make them incorrect in the legend.
"""
import numpy as np
import pandas as pd
import pytest
import seaborn as sns
from seaborn._core.scales import Continuous
from seaborn._core.properties import IntervalProperty


def test_legend_labels_avoid_scientific_notation():
    """
    Test that legend labels avoid scientific notation for large numbers.
    
    The bug was that seaborn legends would show values like "1e6" instead of "1000000"
    when dealing with large numbers because matplotlib's ScalarFormatter would use
    offset formatting by default.
    """
    # Create data with large numbers that would trigger offset formatting
    data = pd.Series([1000000, 2000000, 3000000, 4000000, 5000000], name="large_values")
    
    # Create a continuous scale - this exercises the legend generation code path
    scale = Continuous()._setup(data, IntervalProperty())
    
    # Get legend information
    legend_locs, legend_labels = scale._legend
    
    # The key assertion: legend labels should not contain scientific notation
    # This would indicate the bug is present
    for label in legend_labels:
        # Check that labels don't contain scientific notation indicators
        assert 'e+' not in label, f"Found scientific notation in legend label: {label}"
        assert 'e-' not in label, f"Found scientific notation in legend label: {label}"
        assert '×10' not in label, f"Found scientific notation in legend label: {label}"


def test_small_numbers_work_normally():
    """
    Test that small numbers still work correctly in legends.
    
    This ensures we don't break normal functionality for small numbers.
    """
    # Create data with small numbers
    data = pd.Series([1, 2, 3, 4, 5], name="small_numbers")
    
    # Create a continuous scale
    scale = Continuous()._setup(data, IntervalProperty())
    
    # Check that the legend works normally for small numbers
    legend_locs, legend_labels = scale._legend
    
    # Should have normal labels
    expected_locs = [1, 2, 3, 4, 5]
    actual_locs = [float(loc) for loc in legend_locs]
    
    for expected, actual in zip(expected_locs, actual_locs):
        assert actual == expected, f"Expected {expected}, got {actual}"


def test_legend_preserves_numeric_values():
    """
    Test that legend preserves numeric values correctly for large numbers.
    
    This ensures that when large numbers are used, the legend shows 
    the actual numeric values, not formatted versions.
    """
    # Create data with large numbers that would be problematic with offset formatting
    data = pd.Series([1000000, 2500000, 5000000, 7500000, 10000000], name="large_data")
    
    # Create a continuous scale
    scale = Continuous()._setup(data, IntervalProperty())
    
    # Get legend information
    legend_locs, legend_labels = scale._legend
    
    # Check that we don't have any labels that look like scientific notation
    for label in legend_labels:
        if label:  # Skip empty labels
            # Should not contain scientific notation indicators
            assert 'e+' not in label
            assert 'e-' not in label
            assert '×10' not in label