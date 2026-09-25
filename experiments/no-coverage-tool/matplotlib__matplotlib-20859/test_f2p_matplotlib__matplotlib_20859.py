"""
Regression test for matplotlib bug where adding a legend to a SubFigure doesn't work.

Bug report: Adding a legend to a SubFigure doesn't work
Issue: Legend.__init__ only checks isinstance(parent, Figure) instead of isinstance(parent, FigureBase)
"""
import matplotlib.pyplot as plt
import pytest


def test_legend_on_subfigure_works():
    """Test that legend() can be called on a SubFigure without raising TypeError."""
    # Create a figure and subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create an axes in the subfigure
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should not raise an error
    legend = subfig.legend()
    
    # Verify the legend was created correctly
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"
    
    
def test_legend_on_figure_still_works():
    """Test that legend() still works on regular Figure (regression test)."""
    # Create a regular figure and axes
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work as before
    legend = fig.legend()
    
    # Verify the legend was created correctly
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"


def test_legend_on_axes_still_works():
    """Test that legend() still works on axes (regression test)."""
    # Create axes and plot
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work as before
    legend = ax.legend()
    
    # Verify the legend was created correctly  
    assert legend is not None
    assert len(legend.get_texts()) == 1
    assert legend.get_texts()[0].get_text() == "test"


def test_legend_on_invalid_parent_raises_warning():
    """Test that legend raises warning for invalid parent objects (regression test)."""
    # Create a dummy object that is neither Axes nor Figure
    class Dummy:
        pass
    
    dummy_obj = Dummy()
    
    # This should raise a warning, not a TypeError
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        plt.legend([dummy_obj], ["test"])
        # Should get a warning about unsupported artist
        assert len(w) >= 1
        assert "Legend does not support" in str(w[0].message)