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


def test_plot_directive_template_constants():
    """
    Test that new template constants exist in plot_directive module.
    
    This tests that the TEMPLATE_SRCSET constant was added in the pull request.
    Before the change: constants don't exist
    After the change: constants exist and are accessible
    """
    import matplotlib.sphinxext.plot_directive as plot_module
    
    # Test that the new template constants exist
    assert hasattr(plot_module, 'TEMPLATE_SRCSET')
    assert hasattr(plot_module, '_SOURCECODE')
    
    # Test that the main template still exists (backward compatibility)
    assert hasattr(plot_module, 'TEMPLATE')