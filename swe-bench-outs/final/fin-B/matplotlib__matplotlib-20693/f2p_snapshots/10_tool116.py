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


def test_span_selector_set_props_functionality():
    """Test that set_props method works correctly and modifies properties."""
    ax = get_ax()
    
    def onselect(vmin, vmax):
        pass

    # Create a SpanSelector
    selector = widgets.SpanSelector(ax, onselect, direction='horizontal')
    
    # Verify initial state - check that the selector has the expected initial properties
    initial_props = dict(selector._props)
    assert 'facecolor' in initial_props
    
    # Test that set_props method works and modifies properties correctly
    selector.set_props(facecolor='red', alpha=0.5)
    
    # Verify the properties were updated correctly
    assert selector._props.get('facecolor') == 'red'
    assert selector._props.get('alpha') == 0.5
    
    # Test with another property update
    selector.set_props(edgecolor='black')
    assert selector._props.get('edgecolor') == 'black'


def test_span_selector_set_handle_props_functionality():
    """Test that set_handle_props method works correctly with interactive selectors."""
    ax = get_ax()
    
    def onselect(vmin, vmax):
        pass

    # Create an interactive SpanSelector (this will have handles)
    selector = widgets.SpanSelector(ax, onselect, direction='horizontal', interactive=True)
    
    # Test that set_handle_props method works (should not raise NotImplementedError)
    # This tests the _SelectorWidget.set_handle_props method
    try:
        selector.set_handle_props(color='yellow')
        # If we get here, the method exists and worked
        assert True
    except NotImplementedError:
        # This is expected for selectors without handles, but interactive selectors should have them
        pytest.fail("set_handle_props should work on interactive selectors")
    except AttributeError:
        # This would happen before the change
        pytest.fail("set_handle_props method should exist after the change")