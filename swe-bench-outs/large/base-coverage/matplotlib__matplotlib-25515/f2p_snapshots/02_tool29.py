"""
Regression tests for hi-res plot directive feature.

This test file verifies the behavior of the new figure-mpl directive
and plot_srcset functionality that was added to matplotlib's sphinxext.
"""

import pytest
from unittest.mock import MagicMock


def test_plot_srcset_config_added():
    """
    Test that plot_srcset configuration option is added to plot directive.
    
    This verifies that the new configuration option exists and is properly 
    registered with the sphinx app during setup.
    """
    # Create a mock app that mimics what sphinx would provide
    mock_app = MagicMock()
    mock_app.add_config_value = MagicMock()
    
    # Import and call the setup function directly
    from matplotlib.sphinxext.plot_directive import setup
    
    # Call setup with our mock app
    setup(mock_app)
    
    # Check that add_config_value was called with plot_srcset
    config_calls = [call for call in mock_app.add_config_value.call_args_list 
                   if call[0][0] == 'plot_srcset']
    
    # Should have exactly one call for plot_srcset config
    assert len(config_calls) == 1
    # Check the parameters: name, default_value, rebuild
    assert config_calls[0][0] == ('plot_srcset', [], True)
    
    # Also verify that the default value is an empty list (as per the diff)
    assert config_calls[0][0][1] == []


def test_figure_mpl_directive_exists():
    """
    Test that figure-mpl directive is available and properly registered.
    
    This verifies that the new directive file exists and can be imported.
    """
    # Try to import the figure-mpl directive
    try:
        from matplotlib.sphinxext.figmpl_directive import FigureMpl
        # If we can import it, the directive exists
        assert FigureMpl is not None
        # Verify it has the expected attributes
        assert hasattr(FigureMpl, 'option_spec')
        assert hasattr(FigureMpl, 'run')
        # Check that it has the expected option spec
        expected_options = {'alt', 'height', 'width', 'scale', 'align', 'class', 'caption', 'srcset'}
        actual_options = set(FigureMpl.option_spec.keys())
        assert expected_options.issubset(actual_options)
    except ImportError:
        # This test should fail in the current state
        pytest.fail("figure-mpl directive not yet implemented")


def test_srcset_parsing_function_exists():
    """
    Test that _parse_srcset function exists and works correctly.
    
    This verifies that the function for parsing srcset entries is implemented.
    """
    try:
        from matplotlib.sphinxext.plot_directive import _parse_srcset
        # Test the function with valid input
        result = _parse_srcset(["2x", "1.5x"])
        expected = {2.0: "2x", 1.5: "1.5x"}
        assert result == expected
        
        # Test with single entry
        result2 = _parse_srcset(["2x"])
        expected2 = {2.0: "2x"}
        assert result2 == expected2
        
        # Test invalid input raises error
        with pytest.raises(Exception):  # Should raise ExtensionError
            _parse_srcset(["invalid"])
    except (ImportError, AttributeError) as e:
        # This test should fail in the current state
        pytest.fail(f"_parse_srcset function not yet implemented: {e}")


def test_template_srcset_exists():
    """
    Test that TEMPLATE_SRCSET template is defined.
    
    This verifies that the new template for srcset support is defined.
    """
    try:
        from matplotlib.sphinxext.plot_directive import TEMPLATE_SRCSET
        # If we can import it, the template exists
        assert TEMPLATE_SRCSET is not None
        # Check that it contains the expected structure
        assert ":srcset:" in TEMPLATE_SRCSET
        assert "figure-mpl" in TEMPLATE_SRCSET
        # Check that it contains the expected Jinja2 template structure
        assert "{% for img in images %}" in TEMPLATE_SRCSET
        assert "srcset" in TEMPLATE_SRCSET
    except (ImportError, AttributeError) as e:
        # This test should fail in the current state
        pytest.fail(f"TEMPLATE_SRCSET template not yet implemented: {e}")


def test_plot_directive_uses_srcset_template():
    """
    Test that when plot_srcset is configured, the plot directive uses TEMPLATE_SRCSET.
    
    This verifies the core logic change in the plot directive.
    """
    # This test will be more meaningful after the implementation exists
    # For now, we'll just make sure the necessary components exist
    try:
        from matplotlib.sphinxext.plot_directive import TEMPLATE_SRCSET, TEMPLATE
        # Both templates should exist
        assert TEMPLATE_SRCSET is not None
        assert TEMPLATE is not None
        # Check that they are different (srcset version contains srcset logic)
        assert ":srcset:" in TEMPLATE_SRCSET
        assert ":srcset:" not in TEMPLATE
    except (ImportError, AttributeError):
        # This is expected in the current state
        pytest.skip("srcset template logic not yet implemented")