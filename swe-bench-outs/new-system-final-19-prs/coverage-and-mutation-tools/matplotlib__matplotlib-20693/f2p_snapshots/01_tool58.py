import matplotlib.widgets as widgets
from matplotlib.testing.widgets import do_event, get_ax


def test_rectangle_selector_instantiation():
    """Test that RectangleSelector can be instantiated."""
    ax = get_ax()
    
    def onselect(vmin, vmax):
        pass

    tool = widgets.RectangleSelector(ax, onselect, interactive=True)
    assert tool is not None


def test_span_selector_instantiation():
    """Test that SpanSelector can be instantiated."""
    ax = get_ax()
    
    def onselect(vmin, vmax):
        pass

    tool = widgets.SpanSelector(ax, onselect, 'horizontal', interactive=True)
    assert tool is not None


def test_set_props_functionality():
    """Test that set_props method works (the main fix)."""
    ax = get_ax()
    
    def onselect(vmin, vmax):
        pass

    tool = widgets.RectangleSelector(ax, onselect, interactive=True)
    
    # This should work after the change - the new way to set properties
    # Before the change, this would raise AttributeError
    try:
        tool.set_props(facecolor='red')
        # If we get here without exception, it works
        result = "success"
    except AttributeError:
        result = "failure"
    
    # This assertion is what makes it fail-to-pass
    assert result == "success", "set_props method should work after the change"


def test_set_handle_props_functionality():
    """Test that set_handle_props method works (the main fix)."""
    ax = get_ax()
    
    def onselect(vmin, vmax):
        pass

    tool = widgets.RectangleSelector(ax, onselect, interactive=True)
    
    # This should work after the change - the new way to set handle properties
    # Before the change, this would raise AttributeError
    try:
        tool.set_handle_props(color='blue')
        # If we get here without exception, it works
        result = "success"
    except AttributeError:
        result = "failure"
    
    # This assertion is what makes it fail-to-pass
    assert result == "success", "set_handle_props method should work after the change"


def test_seeded_rectangle_selector_onselect():
    """Test the original functionality still works."""
    ax = get_ax()

    def onselect(vmin, vmax):
        ax._got_onselect = True

    tool = widgets.RectangleSelector(ax, onselect, interactive=True)
    do_event(tool, 'press', xdata=100, ydata=110, button=1)
    # move outside of axis
    do_event(tool, 'onmove', xdata=150, ydata=120, button=1)
    do_event(tool, 'release', xdata=150, ydata=120, button=1)

    assert tool.ax._got_onselect
    assert tool.extents == (100.0, 150.0, 110.0, 120.0)