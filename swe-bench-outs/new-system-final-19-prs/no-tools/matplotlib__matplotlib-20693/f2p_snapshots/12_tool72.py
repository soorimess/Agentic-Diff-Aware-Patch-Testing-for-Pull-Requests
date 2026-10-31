"""
Regression test for the lost functionality of interactive selector update.

This test ensures that the new set_props method works correctly and 
that deprecated functionality still works as expected.
"""

import matplotlib.pyplot as plt
import matplotlib.widgets as widgets


def test_span_selector_new_functionality():
    """
    Test that the new set_props functionality works by testing the exact behavior change.
    """
    fig, ax = plt.subplots()
    
    def onselect(xmin, xmax):
        pass
    
    # Create a span selector
    selector = widgets.SpanSelector(ax, onselect, direction='horizontal')
    
    # Test that we can call set_props without error (this is the main change)
    # The behavior change is that this method should exist and work
    try:
        # This is the exact call that was added in the change
        selector.set_props(facecolor='red', alpha=0.7)
        # If we get here, the method was called successfully
        # The change sets self._props = {'facecolor': 'red', 'alpha': 0.7, 'animated': False}
        expected_props = {'facecolor': 'red', 'alpha': 0.7, 'animated': False}
        assert selector._props == expected_props, f"Expected {expected_props}, got {selector._props}"
        success = True
    except AttributeError:
        success = False
    except Exception as e:
        # Any other exception means it's not working as expected
        success = False
    
    # This assertion tests the exact behavior change
    assert success, "set_props method should work and set the correct properties"
    
    plt.close(fig)


def test_selector_artists_return_value():
    """
    Test that the artists property returns the correct type.
    """
    fig, ax = plt.subplots()
    
    def onselect(xmin, xmax):
        pass
    
    # Create a span selector
    selector = widgets.SpanSelector(ax, onselect, direction='horizontal')
    
    # Test the exact return value that the change produces
    artists = selector.artists
    
    # The change makes this return a tuple instead of a list
    # This is the exact behavior we're testing
    assert type(artists) == tuple, f"Expected tuple, got {type(artists)}"
    
    plt.close(fig)