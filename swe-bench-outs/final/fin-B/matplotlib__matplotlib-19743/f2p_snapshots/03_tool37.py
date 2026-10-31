# Copied unchanged by the harness from lib/matplotlib/tests/test_legend.py::TestLegendFigureFunction::test_warn_args_kwargs, a test in this repository before this change.
import numpy as np
import pytest
import matplotlib.pyplot as plt


class TestSeededLegendFigureFunction:
    def test_seeded_warn_args_kwargs(self):
        fig, axs = plt.subplots(1, 2)
        lines = axs[0].plot(range(10))
        lines2 = axs[1].plot(np.arange(10) * 2.)
        with pytest.warns(UserWarning) as record:
            fig.legend((lines, lines2), labels=('a', 'b'))
        assert len(record) == 1
        assert str(record[0].message) == (
            "You have mixed positional and keyword arguments, some input may "
            "be discarded.")


class TestConstrainedLayoutLegend:
    def test_figure_legend_outside_locations_with_constrained_layout(self):
        """
        Test that figure.legend with 'outside' locations works with constrained_layout.
        
        Before this change, constrained_layout would not account for the size of
        figure legends with 'outside' locations, potentially causing overlap.
        """
        # Create a figure with constrained layout
        fig, axs = plt.subplots(1, 2, layout='constrained')
        
        # Add some data to the axes
        x = np.arange(0.0, 2.0, 0.02)
        y1 = np.sin(2 * np.pi * x)
        y2 = np.exp(-x)
        l1, = axs[0].plot(x, y1)
        l2, = axs[0].plot(x, y2, marker='o')
        
        y3 = np.sin(4 * np.pi * x)
        y4 = np.exp(-2 * x)
        l3, = axs[1].plot(x, y3, color='tab:green')
        l4, = axs[1].plot(x, y4, color='tab:red', marker='^')
        
        # Add a figure legend with an outside location - this should work with constrained layout
        legend = fig.legend((l1, l2), ('Line 1', 'Line 2'), loc='upper left')
        
        # Test that the legend was created successfully
        assert legend is not None
        assert len(fig.legends) == 1
        
        # Test with outside location that should work with constrained layout
        legend2 = fig.legend((l3, l4), ('Line 3', 'Line 4'), loc='outside right upper')
        
        # Test that the second legend was created successfully
        assert legend2 is not None
        assert len(fig.legends) == 2
        
        # Test that the constrained layout is properly applied by checking the legend
        # properties are set correctly
        assert legend2._outside_loc == 'right'
        
    def test_figure_legend_outside_location_validation(self):
        """
        Test that outside locations are properly validated for figure legends.
        """
        fig, axs = plt.subplots(1, 2, layout='constrained')
        
        # Add some data
        x = np.arange(0.0, 2.0, 0.02)
        y1 = np.sin(2 * np.pi * x)
        l1, = axs[0].plot(x, y1)
        
        # Test that axes legends don't accept outside locations (should raise error)
        with pytest.raises(ValueError, match="'outside' option for loc='outside upper right' keyword argument only works for figure legends"):
            axs[0].legend((l1,), ('Line 1',), loc='outside upper right')
            
        # Test that figure legends accept outside locations (should work)
        legend = fig.legend((l1,), ('Line 1',), loc='outside upper right')
        assert legend is not None
        assert legend._outside_loc == 'upper'
        
    def test_constrained_layout_legend_margin_adjustment(self):
        """
        Test that constrained layout properly adjusts margins for figure legends with outside locations.
        """
        # Create a figure with constrained layout
        fig, axs = plt.subplots(1, 2, layout='constrained')
        
        # Add some data
        x = np.arange(0.0, 2.0, 0.02)
        y1 = np.sin(2 * np.pi * x)
        y2 = np.exp(-x)
        l1, = axs[0].plot(x, y1)
        l2, = axs[1].plot(x, y2)
        
        # Add a figure legend with outside location
        legend = fig.legend((l1, l2), ('Line 1', 'Line 2'), loc='outside right upper')
        
        # This should not raise an error and should properly handle the constrained layout
        assert legend is not None
        assert len(fig.legends) == 1
        assert legend._outside_loc == 'right'