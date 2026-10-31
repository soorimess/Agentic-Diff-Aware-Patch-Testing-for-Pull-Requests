"""
Regression test for hi-res plot directive functionality.

This test verifies that the plot directive properly handles the plot_srcset
configuration option to generate responsive images with srcset attributes.
"""

import pytest

# Import the plot directive module to test its behavior
try:
    from matplotlib.sphinxext import plot_directive
    HAS_PLOT_DIRECTIVE = True
except ImportError:
    HAS_PLOT_DIRECTIVE = False


def test_parse_srcset_functionality():
    """
    Test that the _parse_srcset function works correctly.
    
    This tests the core functionality that was added to parse srcset entries.
    Before the PR: this function doesn't exist
    After the PR: this function exists and works correctly
    """
    if not HAS_PLOT_DIRECTIVE:
        pytest.skip("plot_directive module not available")
    
    # Test that the function exists and works correctly
    assert hasattr(plot_directive, '_parse_srcset'), \
        "The _parse_srcset function should exist after the PR"
    
    # Test basic functionality
    result = plot_directive._parse_srcset(['2x'])
    expected = {2.0: '2x'}
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test with multiple entries
    result = plot_directive._parse_srcset(['2x', '1.5x'])
    expected = {2.0: '2x', 1.5: '1.5x'}
    assert result == expected, f"Expected {expected}, got {result}"


def test_sourcecode_constant_exists():
    """
    Test that the _SOURCECODE constant exists and is properly defined.
    
    This tests that the new constant was added to support srcset functionality.
    """
    if not HAS_PLOT_DIRECTIVE:
        pytest.skip("plot_directive module not available")
        
    # Test that the _SOURCECODE constant exists and is not None
    assert hasattr(plot_directive, '_SOURCECODE'), \
        "_SOURCECODE should exist"
        
    # Verify it is not None (this is what matters for functionality)
    assert plot_directive._SOURCECODE is not None, \
        "_SOURCECODE should not be None"
        
    # Test that it's a string (basic sanity check)
    assert isinstance(plot_directive._SOURCECODE, str), \
        "_SOURCECODE should be a string"