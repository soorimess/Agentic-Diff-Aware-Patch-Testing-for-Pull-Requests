import matplotlib.widgets as widgets
from matplotlib.testing.widgets import do_event, get_ax


def test_set_props_works():
    """Test that RectangleSelector.set_props works."""
    ax = get_ax()
    
    def onselect(vmin, vmax):
        pass

    tool = widgets.RectangleSelector(ax, onselect, interactive=True)
    
    # This should not raise an exception after the change
    tool.set_props(facecolor='red')


def test_set_handle_props_works():
    """Test that RectangleSelector.set_handle_props works."""
    ax = get_ax()
    
    def onselect(vmin, vmax):
        pass

    tool = widgets.RectangleSelector(ax, onselect, interactive=True)
    
    # This should not raise an exception after the change
    tool.set_handle_props(color='blue')


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