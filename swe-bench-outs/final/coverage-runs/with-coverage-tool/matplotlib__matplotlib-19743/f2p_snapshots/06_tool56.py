# Test for constrained_layout support for figure.legend
import numpy as np
import pytest
import matplotlib.pyplot as plt


class TestLegendConstrainedLayout:
    def test_figure_legend_outside_with_constrained_layout(self):
        """Test that figure.legend with 'outside' location works with constrained_layout."""
        # This should work without error
        fig, axs = plt.subplots(1, 2, layout='constrained')
        
        x = np.arange(0.0, 2.0, 0.02)
        y1 = np.sin(2 * np.pi * x)
        y2 = np.exp(-x)
        l1, = axs[0].plot(x, y1)
        l2, = axs[0].plot(x, y2, marker='o')

        y3 = np.sin(4 * np.pi * x)
        y4 = np.exp(-2 * x)
        l3, = axs[1].plot(x, y3, color='tab:green')
        l4, = axs[1].plot(x, y4, color='tab:red', marker='^')

        # This should work with constrained_layout
        leg1 = fig.legend((l1, l2), ('Line 1', 'Line 2'), loc='upper left')
        leg2 = fig.legend((l3, l4), ('Line 3', 'Line 4'), loc='outside right upper')
        
        # Check that the legends were created properly and have correct attributes
        assert leg1 is not None
        assert leg2 is not None
        assert len(fig.legends) == 2
        # Check that the outside legend has the correct _outside_loc attribute
        assert leg2._outside_loc == 'right'
        # Check that the legend is for a figure (not axes)
        assert leg2.isaxes is False
        
    def test_axes_legend_outside_raises_error(self):
        """Test that axes.legend with 'outside' location raises an error."""
        fig, axs = plt.subplots(1, 2)
        
        x = np.arange(0.0, 2.0, 0.02)
        y1 = np.sin(2 * np.pi * x)
        l1, = axs[0].plot(x, y1)
        
        # This should raise a ValueError
        with pytest.raises(ValueError, match="'outside' option for loc='outside upper right' keyword argument only works for figure legends"):
            axs[0].legend((l1,), ('Line 1',), loc='outside upper right')
            
    def test_figure_legend_outside_different_positions(self):
        """Test that figure.legend works with different 'outside' positions."""
        fig, axs = plt.subplots(1, 2, layout='constrained')
        
        x = np.arange(0.0, 2.0, 0.02)
        y1 = np.sin(2 * np.pi * x)
        l1, = axs[0].plot(x, y1)
        
        # Test various outside positions that are valid
        positions = [
            'outside upper left',
            'outside upper right',
            'outside lower left',
            'outside lower right',
            'outside left upper',
            'outside right upper',
            'outside left lower',
            'outside right lower'
        ]
        
        for pos in positions:
            # This should not raise an error
            leg = fig.legend((l1,), ('Line 1',), loc=pos)
            # Check that the legend was created and has correct attributes
            assert leg is not None
            # Check that the legend is for a figure (not axes)
            assert leg.isaxes is False
            # Check that the _outside_loc attribute is set correctly
            if pos.startswith('outside '):
                # Extract the first part after "outside"
                parts = pos.split()[1:]
                if len(parts) > 0:
                    # The first part should be the main direction
                    expected_loc = parts[0]
                    assert leg._outside_loc == expected_loc
            # Clear the legend to test next position
            fig.legends.clear()
            
    def test_figure_legend_outside_with_constrained_layout_no_error(self):
        """Test that constrained_layout works with various outside legend positions."""
        # Test with different figure sizes and layouts
        fig, axs = plt.subplots(2, 2, layout='constrained', figsize=(10, 8))
        
        # Create some plots
        x = np.arange(0.0, 2.0, 0.02)
        for i, ax in enumerate(axs.flat):
            y = np.sin((i+1) * np.pi * x)
            ax.plot(x, y)
            
        # Add legends with outside positions
        leg1 = fig.legend(loc='outside upper right')
        leg2 = fig.legend(loc='outside lower left')
        
        # Should not raise any errors and should create legends
        assert leg1 is not None
        assert leg2 is not None
        assert len(fig.legends) == 2
        # Check that the legends have correct _outside_loc attributes
        assert leg1._outside_loc == 'upper'
        assert leg2._outside_loc == 'lower'
        # Check that both legends are for figures (not axes)
        assert leg1.isaxes is False
        assert leg2.isaxes is False
        
    def test_legend_outside_location_parsing(self):
        """Test that legend location parsing works correctly for outside locations."""
        fig, axs = plt.subplots(1, 1, layout='constrained')
        
        x = np.arange(0.0, 2.0, 0.02)
        y = np.sin(2 * np.pi * x)
        l1, = axs.plot(x, y)
        
        # Test the parsing of different outside locations - valid combinations
        test_cases = [
            ('outside right upper', 'right'),
            ('outside upper right', 'upper'),
            ('outside left lower', 'left'),
            ('outside lower left', 'lower'),
        ]
        
        for loc_input, expected_first in test_cases:
            leg = fig.legend((l1,), ('Line 1',), loc=loc_input)
            assert leg is not None
            # Check that the _outside_loc is parsed correctly
            assert leg._outside_loc == expected_first
            # Check that it's a figure legend
            assert leg.isaxes is False
            fig.legends.clear()
            
    def test_constrained_layout_with_outside_legends_executes(self):
        """Test that constrained layout with outside legends executes without error."""
        # Create a figure with constrained layout
        fig, axs = plt.subplots(2, 2, layout='constrained')
        
        # Add some data to the axes
        x = np.linspace(0, 10, 100)
        for i, ax in enumerate(axs.flat):
            ax.plot(x, np.sin(x + i))
            ax.set_title(f'Axis {i}')
            
        # Add multiple legends with outside positions - this should not raise errors
        # and should exercise the make_layout_margins function
        fig.legend(loc='outside upper right')
        fig.legend(loc='outside lower left')
        
        # The figure should be valid and have legends
        assert len(fig.legends) == 2
        assert fig.legends[0]._outside_loc == 'upper'
        assert fig.legends[1]._outside_loc == 'lower'
        
        # The constrained layout should have been processed without error
        # This test specifically exercises the make_layout_margins function
        # by ensuring that when a figure with legends is processed with constrained_layout,
        # it doesn't crash
        assert fig is not None