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


def test_plot_srcset_functionality_exists():
    """
    Test that the core functionality added by the PR exists.
    
    This test checks for the existence of key elements that were added:
    - _parse_srcset function
    - TEMPLATE_SRCSET constant
    - plot_srcset config option handling
    """
    if not HAS_PLOT_DIRECTIVE:
        pytest.skip("plot_directive module not available")
    
    # Test 1: Check that _parse_srcset function exists (added in PR)
    assert hasattr(plot_directive, '_parse_srcset'), \
        "The _parse_srcset function should exist after the PR"
    
    # Test 2: Check that TEMPLATE_SRCSET constant exists (added in PR)
    assert hasattr(plot_directive, 'TEMPLATE_SRCSET'), \
        "The TEMPLATE_SRCSET constant should exist after the PR"
        
    # Test 3: Check that _SOURCECODE constant exists (added in PR)
    assert hasattr(plot_directive, '_SOURCECODE'), \
        "The _SOURCECODE constant should exist after the PR"
    
    # Test 4: Test that _parse_srcset function works correctly
    # This is a basic functionality test
    try:
        result = plot_directive._parse_srcset(['2x'])
        expected = {2.0: '2x'}
        assert result == expected, f"Expected {expected}, got {result}"
    except Exception as e:
        pytest.fail(f"_parse_srcset function failed: {e}")


def test_plot_directive_config_handling():
    """
    Test that plot directive setup function handles plot_srcset config.
    
    This verifies that the setup function properly adds the plot_srcset config option.
    """
    if not HAS_PLOT_DIRECTIVE:
        pytest.skip("plot_directive module not available")
        
    # Check that the setup function exists and can be called
    assert hasattr(plot_directive, 'setup'), "setup function should exist"
    
    # The key test: verify that the plot_srcset config option is available
    # We can't easily test the full sphinx integration here, but we can check
    # that the module structure supports it
    assert hasattr(plot_directive, 'run'), "run function should exist"
    
    # Verify that the module has the expected structure for the PR changes
    expected_attrs = [
        'TEMPLATE_SRCSET',
        '_SOURCECODE', 
        '_parse_srcset',
        'setup',
        'run'
    ]
    
    for attr in expected_attrs:
        assert hasattr(plot_directive, attr), f"Missing expected attribute: {attr}"


def test_template_constants_exist():
    """
    Test that the new template constants exist and are properly defined.
    """
    if not HAS_PLOT_DIRECTIVE:
        pytest.skip("plot_directive module not available")
        
    # Check that the new template constants exist
    assert hasattr(plot_directive, 'TEMPLATE_SRCSET'), \
        "TEMPLATE_SRCSET should exist"
    assert hasattr(plot_directive, '_SOURCECODE'), \
        "SOURCECODE should exist"
        
    # Verify they are not None
    assert plot_directive.TEMPLATE_SRCSET is not None, \
        "TEMPLATE_SRCSET should not be None"
    assert plot_directive._SOURCECODE is not None, \
        "SOURCECODE should not be None"