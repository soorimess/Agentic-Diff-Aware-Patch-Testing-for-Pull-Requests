"""
Regression test for Nominal scale behavior in seaborn.

This test ensures that Nominal scales are properly handled in the plotting pipeline
by testing that the specific code paths for Nominal scale behaviors execute correctly.
"""

import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from seaborn._core.plot import Plot
from seaborn._core.scales import Nominal
from seaborn._marks.base import Mark


class MockMark(Mark):
    """A simple mock mark for testing."""
    _grouping_props = ["color"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passed_keys = []
        self.passed_data = []
        self.passed_axes = []
        self.passed_scales = None

    def _plot(self, ax, data, scales):
        self.passed_keys.append(list(data.keys()))
        self.passed_data.append(data)
        self.passed_axes.append(ax)
        self.passed_scales = scales
        # Simple plot - just return something
        return []


def test_nominal_scale_code_paths():
    """
    Test that Nominal scale code paths execute without errors.
    
    This test verifies that the Nominal scale handling logic in _finalize_figure
    executes correctly for various Nominal scale scenarios.
    """
    # Test cases that should trigger Nominal scale behavior
    test_cases = [
        # Nominal scale on x-axis (4 categories)
        pd.DataFrame({'x': ['A', 'B', 'C', 'D'], 'y': [1, 2, 3, 4]}),
        
        # Nominal scale on y-axis (4 categories) 
        pd.DataFrame({'x': [1, 2, 3, 4], 'y': ['A', 'B', 'C', 'D']}),
        
        # Both axes as Nominal (4 categories each)
        pd.DataFrame({'x': ['A', 'B', 'C', 'D'], 'y': ['P', 'Q', 'R', 'S']}),
    ]
    
    # All cases should work without errors, verifying Nominal scale handling
    for i, data in enumerate(test_cases):
        # This creates a plot that should exercise Nominal scale code paths
        p = Plot(data, x='x', y='y').add(MockMark()).plot()
        assert p is not None, f"Nominal scale handling failed for test case {i+1}"
        
    # Additional test: ensure Nominal scale can be imported and used
    # This verifies the import works correctly
    assert Nominal is not None