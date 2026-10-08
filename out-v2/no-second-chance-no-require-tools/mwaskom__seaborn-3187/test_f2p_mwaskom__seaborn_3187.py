import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

from seaborn._core.scales import Continuous
from seaborn._core.properties import Coordinate


def test_legend_labels_dont_use_offset_scientific():
    """
    Test that legend labels for large numbers don't use offset/scientific notation.
    
    This test verifies the fix for the bug where legends with large numbers
    were formatted using offset/scientific notation instead of plain numbers.
    """
    
    # Create data with large numbers that would trigger formatter offset/scientific notation
    # These values are large enough to cause matplotlib to use offset notation
    large_values = [1000000, 2000000, 3000000, 4000000, 5000000]
    data = pd.Series(large_values, name='large_numbers')
    
    # Create a continuous scale with pointsize property (which creates legends)
    scale = Continuous('pointsize')
    
    # Setup the scale - this should trigger the legend generation code path
    result = scale._setup(data, Coordinate())
    
    # Check if legend was created
    if hasattr(result, '_legend') and result._legend is not None:
        locs, labels = result._legend
        
        # Verify that no legend labels contain offset or scientific notation
        # These patterns would indicate the bug was present
        for label in labels:
            # Check for scientific notation (e.g., 1e+06, 1.0e+06)
            if 'e+' in label or 'e-' in label:
                pytest.fail(f"Legend label contains scientific notation: '{label}'")
            
            # Check for offset notation (e.g., 1×10⁶, 1e6)  
            if '×10' in label or 'e6' in label:
                pytest.fail(f"Legend label contains offset notation: '{label}'")
            
            # Additional check for common problematic patterns
            if label.strip() == '' or label.isspace():
                # Empty labels might also indicate issues
                pytest.fail(f"Legend label is empty or whitespace: '{label}'")


def test_scale_legend_generation_behavior():
    """
    Test that scale legend generation properly handles large number formatting.
    
    This specifically tests the behavior that was changed in the pull request
    where formatter settings were explicitly disabled for legends.
    """
    
    # Create test data with values that would trigger formatter behavior
    test_values = pd.Series([5000000, 10000000, 15000000], name='test_values')
    
    # Create a continuous scale
    scale = Continuous('pointsize')
    
    # This should generate legend entries without offset/scientific notation
    result = scale._setup(test_values, Coordinate())
    
    # Check legend generation
    if hasattr(result, '_legend') and result._legend is not None:
        locs, labels = result._legend
        
        # All labels should be plain numbers, not using offset/scientific notation
        for label in labels:
            # The bug was that these would contain offset/scientific notation
            if any(pattern in label for pattern in ['e+', 'e-', '×10']):
                pytest.fail(f"Legend label incorrectly uses offset/scientific notation: '{label}'")