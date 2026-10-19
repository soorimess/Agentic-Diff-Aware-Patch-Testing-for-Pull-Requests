"""
Regression test for interactive selector update functionality.

This test ensures that the old API for selector properties works correctly
and emits appropriate deprecation warnings, preserving backward compatibility
after the PR that fixes lost functionality.

The test specifically verifies the behavior described in the issue where
MNE users were doing:
    selector.rect.set_color(color)
    selector.rectprops.update(dict(facecolor=color))
    
These patterns should continue to work with proper deprecation warnings.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import warnings
from matplotlib.widgets import SpanSelector


def test_span_selector_old_api_functionality():
    """
    Test that the old selector API functionality works correctly.
    
    This test verifies that the exact patterns mentioned in the issue report
    continue to work with appropriate deprecation warnings.
    """
    fig, ax = plt.subplots()
    
    def onselect(xmin, xmax):
        pass
    
    # Create a span selector
    selector = SpanSelector(ax, onselect, 'horizontal')
    
    # Test 1: Access rect property should work and emit deprecation warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        rect = selector.rect
        assert rect is not None, "selector.rect should be accessible"
        
        # Verify deprecation warning is issued for rect access
        deprecation_warnings = [warning for warning in w if "deprecated" in str(warning.message).lower()]
        assert len(deprecation_warnings) >= 1, "Should emit deprecation warning for rect access"
    
    # Test 2: Set color on rect should work and emit deprecation warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        # This is the exact pattern from the issue report
        selector.rect.set_color('red')
        
        # Verify deprecation warning is issued
        deprecation_warnings = [warning for warning in w if "deprecated" in str(warning.message).lower()]
        assert len(deprecation_warnings) >= 1, "Should emit deprecation warning when setting rect color"
    
    # Test 3: Update rectprops should work and emit deprecation warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        # This is the exact pattern from the issue report
        selector.rectprops.update(dict(facecolor='blue'))
        
        # Verify deprecation warning is issued
        deprecation_warnings = [warning for warning in w if "deprecated" in str(warning.message).lower()]
        assert len(deprecation_warnings) >= 1, "Should emit deprecation warning when updating rectprops"
    
    plt.close(fig)


def test_span_selector_internal_structure():
    """
    Test that internal artist structure works correctly.
    """
    fig, ax = plt.subplots()
    
    def onselect(xmin, xmax):
        pass
    
    # Create a span selector
    selector = SpanSelector(ax, onselect, 'horizontal')
    
    # Test that we can access internal artists without error
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        artists = selector.artists
        assert len(artists) >= 1, "Should have at least one artist"
    
    plt.close(fig)