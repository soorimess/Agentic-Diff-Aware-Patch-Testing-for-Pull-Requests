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


# Copied unchanged by the harness from lib/matplotlib/tests/test_widgets.py::test_polygon_selector, a test in this repository before this change.
import matplotlib.widgets as widgets
from matplotlib.testing.widgets import do_event, get_ax


def check_polygon_selector(event_sequence, expected_result, selections_count):
    """
    Helper function to test Polygon Selector.

    Parameters
    ----------
    event_sequence : list of tuples (etype, dict())
        A sequence of events to perform. The sequence is a list of tuples
        where the first element of the tuple is an etype (e.g., 'onmove',
        'press', etc.), and the second element of the tuple is a dictionary of
         the arguments for the event (e.g., xdata=5, key='shift', etc.).
    expected_result : list of vertices (xdata, ydata)
        The list of vertices that are expected to result from the event
        sequence.
    selections_count : int
        Wait for the tool to call its `onselect` function `selections_count`
        times, before comparing the result to the `expected_result`
    """
    ax = get_ax()

    ax._selections_count = 0

    def onselect(vertices):
        ax._selections_count += 1
        ax._current_result = vertices

    tool = widgets.PolygonSelector(ax, onselect)

    for (etype, event_args) in event_sequence:
        do_event(tool, etype, **event_args)

    assert ax._selections_count == selections_count
    assert ax._current_result == expected_result


def polygon_place_vertex(xdata, ydata):
    return [('onmove', dict(xdata=xdata, ydata=ydata)),
            ('press', dict(xdata=xdata, ydata=ydata)),
            ('release', dict(xdata=xdata, ydata=ydata))]


def test_seeded_polygon_selector():
    # Simple polygon
    expected_result = [(50, 50), (150, 50), (50, 150)]
    event_sequence = (polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(50, 50))
    check_polygon_selector(event_sequence, expected_result, 1)

    # Move first vertex before completing the polygon.
    expected_result = [(75, 50), (150, 50), (50, 150)]
    event_sequence = (polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + [('on_key_press', dict(key='control')),
                         ('onmove', dict(xdata=50, ydata=50)),
                         ('press', dict(xdata=50, ydata=50)),
                         ('onmove', dict(xdata=75, ydata=50)),
                         ('release', dict(xdata=75, ydata=50)),
                         ('on_key_release', dict(key='control'))]
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(75, 50))
    check_polygon_selector(event_sequence, expected_result, 1)

    # Move first two vertices at once before completing the polygon.
    expected_result = [(50, 75), (150, 75), (50, 150)]
    event_sequence = (polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + [('on_key_press', dict(key='shift')),
                         ('onmove', dict(xdata=100, ydata=100)),
                         ('press', dict(xdata=100, ydata=100)),
                         ('onmove', dict(xdata=100, ydata=125)),
                         ('release', dict(xdata=100, ydata=125)),
                         ('on_key_release', dict(key='shift'))]
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(50, 75))
    check_polygon_selector(event_sequence, expected_result, 1)

    # Move first vertex after completing the polygon.
    expected_result = [(75, 50), (150, 50), (50, 150)]
    event_sequence = (polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(50, 50)
                      + [('onmove', dict(xdata=50, ydata=50)),
                         ('press', dict(xdata=50, ydata=50)),
                         ('onmove', dict(xdata=75, ydata=50)),
                         ('release', dict(xdata=75, ydata=50))])
    check_polygon_selector(event_sequence, expected_result, 2)

    # Move all vertices after completing the polygon.
    expected_result = [(75, 75), (175, 75), (75, 175)]
    event_sequence = (polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(50, 50)
                      + [('on_key_press', dict(key='shift')),
                         ('onmove', dict(xdata=100, ydata=100)),
                         ('press', dict(xdata=100, ydata=100)),
                         ('onmove', dict(xdata=125, ydata=125)),
                         ('release', dict(xdata=125, ydata=125)),
                         ('on_key_release', dict(key='shift'))])
    check_polygon_selector(event_sequence, expected_result, 2)

    # Try to move a vertex and move all before placing any vertices.
    expected_result = [(50, 50), (150, 50), (50, 150)]
    event_sequence = ([('on_key_press', dict(key='control')),
                       ('onmove', dict(xdata=100, ydata=100)),
                       ('press', dict(xdata=100, ydata=100)),
                       ('onmove', dict(xdata=125, ydata=125)),
                       ('release', dict(xdata=125, ydata=125)),
                       ('on_key_release', dict(key='control')),
                       ('on_key_press', dict(key='shift')),
                       ('onmove', dict(xdata=100, ydata=100)),
                       ('press', dict(xdata=100, ydata=100)),
                       ('onmove', dict(xdata=125, ydata=125)),
                       ('release', dict(xdata=125, ydata=125)),
                       ('on_key_release', dict(key='shift'))]
                      + polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(50, 50))
    check_polygon_selector(event_sequence, expected_result, 1)

    # Try to place vertex out-of-bounds, then reset, and start a new polygon.
    expected_result = [(50, 50), (150, 50), (50, 150)]
    event_sequence = (polygon_place_vertex(50, 50)
                      + polygon_place_vertex(250, 50)
                      + [('on_key_press', dict(key='escape')),
                         ('on_key_release', dict(key='escape'))]
                      + polygon_place_vertex(50, 50)
                      + polygon_place_vertex(150, 50)
                      + polygon_place_vertex(50, 150)
                      + polygon_place_vertex(50, 50))
    check_polygon_selector(event_sequence, expected_result, 1)
