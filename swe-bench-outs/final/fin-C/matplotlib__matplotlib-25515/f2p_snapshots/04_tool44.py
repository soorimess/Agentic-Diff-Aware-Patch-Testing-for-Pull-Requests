"""
Regression test for hi-res plot directive functionality.

This test verifies the behavior changes introduced by the pull request
that adds support for hi-res plot directive with srcset image options.
"""
import pytest


def test_srcset_functionality_exists():
    """
    Test that the _parse_srcset function exists and works correctly.
    
    Before the change: this function doesn't exist, so the import will fail
    After the change: this function exists and works as expected
    """
    # Import the function directly to test it
    from matplotlib.sphinxext.plot_directive import _parse_srcset
    
    # Test the function with valid inputs
    result = _parse_srcset(["2x", "1.5x"])
    expected = {2.0: "2x", 1.5: "1.5x"}
    assert result == expected
    
    # Test with single entry
    result = _parse_srcset(["3x"])
    expected = {3.0: "3x"}
    assert result == expected


def test_plot_directive_constants_exist():
    """
    Test that new template constants exist in plot_directive module.
    
    Before the change: these constants don't exist
    After the change: these constants exist
    """
    import matplotlib.sphinxext.plot_directive as plot_module
    
    # Test that the new template constants exist
    assert hasattr(plot_module, 'TEMPLATE_SRCSET')
    assert hasattr(plot_module, '_SOURCECODE')
    
    # Test that the main template still exists
    assert hasattr(plot_module, 'TEMPLATE')