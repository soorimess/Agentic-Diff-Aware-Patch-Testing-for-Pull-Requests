"""
Regression test for the lost functionality of interactive selector update.

This test ensures that the new set_props method works correctly and 
that deprecated functionality still works as expected.
"""

import matplotlib.pyplot as plt
import matplotlib.widgets as widgets


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
    
    # Verify the exact behavior that was changed - the method sets specific properties
    # The change specifically sets self._props = {'facecolor': 'red', 'alpha': 0.7, 'animated': False}
    expected_props = {'facecolor': 'red', 'alpha': 0.7, 'animated': False}
    assert selector._props == expected_props
    
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
    
    # Test that the artists property returns what we expect - a tuple instead of list
    artists = selector.artists
    # The change makes this return a tuple instead of a list
    # This is the exact behavior change we're testing
    assert type(artists) == tuple
    assert len(artists) >= 1
    assert hasattr(artists[0], 'set_visible')
    
    plt.close(fig)