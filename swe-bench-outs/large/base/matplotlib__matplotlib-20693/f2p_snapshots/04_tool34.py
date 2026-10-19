"""
Test for regression of interactive selector update functionality.

This test ensures that the deprecated rect and rectprops attributes still work
and that the new set_props method functions correctly.
"""
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import pytest
from matplotlib._api.deprecation import MatplotlibDeprecationWarning


def test_span_selector_rect_deprecation():
    """Test that accessing rect property still works (deprecated)"""
    fig, ax = plt.subplots()
    try:
        def onselect(vmin, vmax):
            pass
            
        selector = widgets.SpanSelector(ax, onselect, 'horizontal')
        
        # This should work but emit a deprecation warning
        # The issue mentioned that this used to work but now emits deprecation warning
        with pytest.warns(MatplotlibDeprecationWarning):
            rect = selector.rect
            
        # Test that we can still set properties on the rect (this is what user was doing)
        # This should work but emit a deprecation warning
        with pytest.warns(MatplotlibDeprecationWarning):
            selector.rect.set_color('red')
            
    finally:
        plt.close(fig)


def test_span_selector_rectprops_deprecation():
    """Test that accessing rectprops property still works (deprecated)"""
    fig, ax = plt.subplots()
    try:
        def onselect(vmin, vmax):
            pass
            
        selector = widgets.SpanSelector(ax, onselect, 'horizontal')
        
        # This should work but emit a deprecation warning
        with pytest.warns(MatplotlibDeprecationWarning):
            props = selector.rectprops
            
        # Test that we can still update rectprops (this is what user was doing)
        with pytest.warns(MatplotlibDeprecationWarning):
            selector.rectprops.update({'facecolor': 'blue'})
            
    finally:
        plt.close(fig)


def test_span_selector_set_props_method():
    """Test that the new set_props method works (after change)"""
    fig, ax = plt.subplots()
    try:
        def onselect(vmin, vmax):
            pass
            
        selector = widgets.SpanSelector(ax, onselect, 'horizontal')
        
        # This method should exist after the change
        # For now, we'll check that it exists and works
        assert hasattr(selector, 'set_props')
        
        # Test that it works
        selector.set_props(facecolor='green')
        
        # Verify the property was set
        assert selector._props['facecolor'] == 'green'
        
    finally:
        plt.close(fig)


def test_span_selector_set_handle_props_method():
    """Test that the new set_handle_props method works (after change)"""
    fig, ax = plt.subplots()
    try:
        def onselect(vmin, vmax):
            pass
            
        selector = widgets.SpanSelector(ax, onselect, 'horizontal', interactive=True)
        
        # This method should exist after the change
        assert hasattr(selector, 'set_handle_props')
        
        # Test that it works
        selector.set_handle_props(color='yellow')
        
        # Verify the property was set
        assert selector._handle_props['color'] == 'yellow'
        
    finally:
        plt.close(fig)


def test_span_selector_artists_property():
    """Test that the new artists property works (after change)"""
    fig, ax = plt.subplots()
    try:
        def onselect(vmin, vmax):
            pass
            
        selector = widgets.SpanSelector(ax, onselect, 'horizontal')
        
        # This property should exist after the change
        assert hasattr(selector, 'artists')
        
        # Test that it returns a tuple (not a list)
        artists = selector.artists
        assert isinstance(artists, tuple)
        
        # Test that it contains at least one artist
        assert len(artists) >= 1
        
        # Test that the first artist is the selection artist
        assert hasattr(artists[0], 'set_visible')
        
    finally:
        plt.close(fig)


def test_span_selector_direction_change():
    """Test that direction change works with new _selection_artist (after change)"""
    fig, ax = plt.subplots()
    try:
        def onselect(vmin, vmax):
            pass
            
        selector = widgets.SpanSelector(ax, onselect, 'horizontal')
        
        # Test that we can change direction (this uses _selection_artist)
        selector.direction = 'vertical'
        
        # Verify the direction changed
        assert selector.direction == 'vertical'
        
    finally:
        plt.close(fig)


def test_span_selector_handle_props_with_handles():
    """Test set_handle_props when handles exist"""
    fig, ax = plt.subplots()
    try:
        def onselect(vmin, vmax):
            pass
            
        selector = widgets.SpanSelector(ax, onselect, 'horizontal', interactive=True)
        
        # This should work when handles exist
        selector.set_handle_props(color='purple')
        
        # Verify the property was set
        assert selector._handle_props['color'] == 'purple'
        
    finally:
        plt.close(fig)


def test_span_selector_set_props_with_blit():
    """Test set_props with useblit=True"""
    fig, ax = plt.subplots()
    try:
        def onselect(vmin, vmax):
            pass
            
        selector = widgets.SpanSelector(ax, onselect, 'horizontal', useblit=True)
        
        # Test that set_props works with blit
        selector.set_props(facecolor='orange')
        
        # Verify the property was set
        assert selector._props['facecolor'] == 'orange'
        
    finally:
        plt.close(fig)


def test_span_selector_selection_artist_access():
    """Test direct access to _selection_artist works"""
    fig, ax = plt.subplots()
    try:
        def onselect(vmin, vmax):
            pass
            
        selector = widgets.SpanSelector(ax, onselect, 'horizontal')
        
        # Test that _selection_artist exists and can be accessed
        assert hasattr(selector, '_selection_artist')
        
        # Test that it has the expected methods
        assert hasattr(selector._selection_artist, 'set_x')
        assert hasattr(selector._selection_artist, 'set_width')
        assert hasattr(selector._selection_artist, 'set_visible')
        
    finally:
        plt.close(fig)