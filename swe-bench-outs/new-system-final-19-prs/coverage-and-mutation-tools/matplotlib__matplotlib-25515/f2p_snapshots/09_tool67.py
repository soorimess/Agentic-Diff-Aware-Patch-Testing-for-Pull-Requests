"""
Regression test for hi-res plot directive functionality.

This test verifies the behavior changes introduced by the pull request
that adds support for hi-res plot directive with srcset image options.
"""

def test_parse_srcset_function():
    """
    Test that _parse_srcset function works correctly.
    
    This function was added in the pull request to parse srcset entries.
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


def test_plot_directive_structure():
    """
    Test that plot directive has new structure for srcset support.
    
    Tests that the new TEMPLATE_SRCSET constant exists and the basic 
    structure is in place.
    """
    import matplotlib.sphinxext.plot_directive as plot_module
    
    # Test that the new template constants exist (this is part of the change)
    assert hasattr(plot_module, 'TEMPLATE_SRCSET')
    assert hasattr(plot_module, '_SOURCECODE')
    
    # Test that the main template still exists (backward compatibility)
    assert hasattr(plot_module, 'TEMPLATE')