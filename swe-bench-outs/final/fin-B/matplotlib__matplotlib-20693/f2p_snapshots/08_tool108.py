import matplotlib.widgets as widgets
from matplotlib.testing.widgets import do_event, get_ax
import pytest
import warnings


@pytest.mark.parametrize('interactive', [True, False])
def test_seeded_rectangle_selector_onselect(interactive):
    # check when press and release events take place at the same position
    ax = get_ax()

    def onselect(vmin, vmax):
        ax._got_onselect = True

    tool = widgets.RectangleSelector(ax, onselect, interactive=interactive)
    do_event(tool, 'press', xdata=100, ydata=110, button=1)
    # move outside of axis
    do_event(tool, 'onmove', xdata=150, ydata=120, button=1)
    do_event(tool, 'release', xdata=150, ydata=120, button=1)

    assert tool.ax._got_onselect
    assert tool.extents == (100.0, 150.0, 110.0, 120.0)

    # Reset tool.ax._got_onselect
    tool.ax._got_onselect = False

    do_event(tool, 'press', xdata=10, ydata=100, button=1)
    do_event(tool, 'release', xdata=10, ydata=100, button=1)

    assert tool.ax._got_onselect


def test_span_selector_rect_deprecation_behavior():
    """Test that accessing rect property issues correct deprecation warning."""
    ax = get_ax()
    
    def onselect(vmin, vmax):
        pass

    # Create a SpanSelector
    selector = widgets.SpanSelector(ax, onselect, direction='horizontal')
    
    # Test that accessing rect property issues the correct deprecation warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        # This should work but issue a deprecation warning
        rect = selector.rect
        # Should have issued a deprecation warning
        assert len(w) >= 1
        # Check that it's a deprecation warning with the right message
        deprecation_warnings = [warning for warning in w if "deprecated" in str(warning.message).lower()]
        assert len(deprecation_warnings) >= 1
        # The rect should be a valid artist object (not None)
        assert rect is not None


def test_span_selector_set_props_exists():
    """Test that set_props method exists and works (fail-to-pass test)."""
    ax = get_ax()
    
    def onselect(vmin, vmax):
        pass

    # Create a SpanSelector
    selector = widgets.SpanSelector(ax, onselect, direction='horizontal')
    
    # This call should not raise AttributeError - that's our test
    # If it fails before the change, it will raise AttributeError  
    # If it passes after the change, it will work
    selector.set_props(facecolor='red')
    
    # Verify it actually worked by checking the property was set
    assert selector._props.get('facecolor') == 'red'