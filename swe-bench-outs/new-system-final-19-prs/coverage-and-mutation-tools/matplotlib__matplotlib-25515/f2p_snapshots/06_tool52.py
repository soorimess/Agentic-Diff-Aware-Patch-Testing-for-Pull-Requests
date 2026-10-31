"""
Regression test for hi-res plot directive functionality.

This test verifies the behavior changes introduced by the pull request
that adds support for hi-res plot directive with srcset image options.
"""

def test_parse_srcset_function():
    """
    Test that _parse_srcset function works correctly.
    
    This function was added in the pull request to parse srcset entries.
    Before the change: function doesn't exist
    After the change: function exists and returns correct dictionary
    """
    # Import the function that was added
    from matplotlib.sphinxext.plot_directive import _parse_srcset
    
    # Test with multiple entries
    result = _parse_srcset(["2x", "1.5x"])
    expected = {2.0: "2x", 1.5: "1.5x"}
    assert result == expected
    
    # Test with single entry
    result = _parse_srcset(["3x"])
    expected = {3.0: "3x"}
    assert result == expected


def test_figmpl_directive_module_exists():
    """
    Test that the figure-mpl directive module exists and has key components.
    
    This module was added in the pull request to support responsive images.
    Before the change: module doesn't exist
    After the change: module exists with FigureMpl class and related functions
    """
    # Import the module that was added
    from matplotlib.sphinxext import figmpl_directive
    
    # Test that the main classes and functions exist
    assert hasattr(figmpl_directive, 'FigureMpl')
    assert hasattr(figmpl_directive, 'figmplnode')
    assert hasattr(figmpl_directive, 'visit_figmpl_html')
    assert hasattr(figmpl_directive, 'visit_figmpl_latex')