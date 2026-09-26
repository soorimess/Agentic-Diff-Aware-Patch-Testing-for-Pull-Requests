"""
Test for matplotlib issue #20859: Adding a legend to a SubFigure doesn't work

This test verifies that legends can be added to SubFigure objects,
which was broken before the fix.
"""
import matplotlib.pyplot as plt
import pytest


def test_legend_on_subfigure():
    """Test that a legend can be added to a SubFigure."""
    # Create a figure with subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create an axes within the subfigure
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should work but currently raises TypeError
    # "Legend needs either Axes or Figure as parent"
    try:
        subfig.legend()
        # If we get here without exception, the test passes
        assert True
    except TypeError as e:
        if "Legend needs either Axes or Figure as parent" in str(e):
            pytest.fail("Adding legend to SubFigure failed with TypeError")
        else:
            raise  # Re-raise if it's a different TypeError


def test_legend_on_subfigure_with_handles_labels():
    """Test that a legend can be added to a SubFigure with explicit handles and labels."""
    # Create a figure with subfigures
    fig = plt.figure()
    subfig = fig.subfigures()
    
    # Create an axes within the subfigure
    ax = subfig.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # Get handles and labels from the axes
    handles, labels = ax.get_legend_handles_labels()
    
    # This should work but currently raises TypeError
    # "Legend needs either Axes or Figure as parent"
    try:
        subfig.legend(handles, labels)
        # If we get here without exception, the test passes
        assert True
    except TypeError as e:
        if "Legend needs either Axes or Figure as parent" in str(e):
            pytest.fail("Adding legend to SubFigure with handles/labels failed with TypeError")
        else:
            raise  # Re-raise if it's a different TypeError


def test_legend_on_figure_still_works():
    """Test that legends still work on regular Figure objects (regression test)."""
    # Create a regular figure
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should continue to work
    try:
        fig.legend()
        assert True
    except Exception as e:
        pytest.fail(f"Adding legend to regular Figure failed: {e}")


def test_legend_on_axes_still_works():
    """Test that legends still work on axes objects (regression test)."""
    # Create an axes
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 2], label="test")
    
    # This should continue to work
    try:
        ax.legend()
        assert True
    except Exception as e:
        pytest.fail(f"Adding legend to axes failed: {e}")


if __name__ == "__main__":
    # Run the tests directly
    test_legend_on_subfigure()
    test_legend_on_subfigure_with_handles_labels()
    test_legend_on_figure_still_works()
    test_legend_on_axes_still_works()
    print("All tests passed!")