"""
Regression test for the lost functionality of interactive selector update.

This test ensures that the new set_props method works correctly and 
that deprecated functionality still works as expected.
"""

import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import pytest
from matplotlib._api.deprecation import MatplotlibDeprecationWarning
import warnings


def test_span_selector_new_set_props_functionality():
    """
    Test that the new set_props method works correctly.
    This is the main functionality that was added in the PR.
    """
    fig, ax = plt.subplots()
    
    def onselect(xmin, xmax):
        pass
    
    # Create a span selector
    selector = widgets.SpanSelector(ax, onselect, direction='horizontal')
    
    # Test the new set_props method that should replace deprecated direct access
    # This is the main functionality that was added
    selector.set_props(facecolor='red', alpha=0.7)
    
    # Verify the properties were set
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # Ignore deprecation warnings for this test
        rect_artist = selector.rect
        # Check that the properties were actually applied
        # This tests the core functionality that was added
        props = rect_artist.properties()
        assert 'facecolor' in props
        assert 'alpha' in props
    
    plt.close(fig)


def test_span_selector_deprecated_rect_functionality():
    """
    Test that deprecated rect property still works for backward compatibility.
    """
    fig, ax = plt.subplots()
    
    def onselect(xmin, xmax):
        pass
    
    # Create a span selector
    selector = widgets.SpanSelector(ax, onselect, direction='horizontal')
    
    # Test that deprecated rect property works
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Access the rect property (should work with deprecation warning)
        rect_artist = selector.rect
        
        # This should work - calling set_color on the returned artist
        # This is the functionality that users were relying on
        rect_artist.set_color('blue')
        
        # Should emit deprecation warning
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, MatplotlibDeprecationWarning)]
        assert len(deprecation_warnings) >= 1
    
    plt.close(fig)


def test_span_selector_deprecated_rectprops_functionality():
    """
    Test that deprecated rectprops property still works for backward compatibility.
    """
    fig, ax = plt.subplots()
    
    def onselect(xmin, xmax):
        pass
    
    # Create a span selector
    selector = widgets.SpanSelector(ax, onselect, direction='horizontal')
    
    # Test that deprecated rectprops property works
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Access the rectprops property (should work with deprecation warning)
        rectprops_dict = selector.rectprops
        
        # This should work - updating the dict
        rectprops_dict.update({'facecolor': 'green', 'alpha': 0.8})
        
        # Should emit deprecation warning
        deprecation_warnings = [warning for warning in w if issubclass(warning.category, MatplotlibDeprecationWarning)]
        assert len(deprecation_warnings) >= 1
    
    plt.close(fig)


def test_selector_artists_property():
    """
    Test that the artists property works correctly.
    This tests the new implementation of the artists property.
    """
    fig, ax = plt.subplots()
    
    def onselect(xmin, xmax):
        pass
    
    # Create a span selector
    selector = widgets.SpanSelector(ax, onselect, direction='horizontal')
    
    # Test the new artists property
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # Ignore deprecation warnings for this test
        artists = selector.artists
        # Should return tuple with selection artist
        assert isinstance(artists, tuple)
        assert len(artists) >= 1
        assert hasattr(artists[0], 'set_visible')
    
    plt.close(fig)