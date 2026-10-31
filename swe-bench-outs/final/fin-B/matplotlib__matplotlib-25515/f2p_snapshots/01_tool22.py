"""
Test for the hi-res plot directive enhancement.

This test verifies the behavior of the new plot_srcset functionality
that allows creating responsive hi-DPI images for sphinx documentation.
"""

import pytest
from unittest.mock import MagicMock


def test_plot_directive_has_srcset_config():
    """
    Test that plot_srcset configuration option is properly added to the extension.
    
    Before the change: This test fails because plot_srcset config is not added
    After the change: This test passes because plot_srcset config is added
    """
    # Import the setup function
    from matplotlib.sphinxext.plot_directive import setup
    
    # Create a mock Sphinx app
    mock_app = MagicMock()
    
    # Call setup - this should properly register the plot_srcset config
    setup(mock_app)
    
    # Verify that add_config_value was called with the right parameters
    # This is the core behavior that changes
    mock_app.add_config_value.assert_any_call('plot_srcset', [], True)


def test_figure_mpl_directive_module_exists():
    """
    Test that the figure-mpl directive module exists and is importable.
    
    Before the change: This test fails because figmpl_directive.py doesn't exist
    After the change: This test passes because figmpl_directive.py exists
    """
    # This should work after the change
    import matplotlib.sphinxext.figmpl_directive
    
    # Check that key components exist
    assert hasattr(matplotlib.sphinxext.figmpl_directive, 'FigureMpl')
    assert hasattr(matplotlib.sphinxext.figmpl_directive, 'setup')
    assert hasattr(matplotlib.sphinxext.figmpl_directive, 'figmplnode')


def test_plot_directive_has_template_constants():
    """
    Test that the new template constants exist in plot_directive.
    
    Before the change: This test fails because TEMPLATE_SRCSET doesn't exist
    After the change: This test passes because TEMPLATE_SRCSET exists
    """
    # These should exist after the change
    from matplotlib.sphinxext.plot_directive import TEMPLATE_SRCSET, TEMPLATE
    
    # Both should be defined and different
    assert TEMPLATE_SRCSET is not None
    assert TEMPLATE is not None
    assert TEMPLATE_SRCSET != TEMPLATE


def test_parse_srcset_function_exists():
    """
    Test that _parse_srcset function exists and works.
    
    Before the change: This test fails because _parse_srcset doesn't exist
    After the change: This test passes because _parse_srcset exists and works
    """
    # Import the function that should exist after the change
    from matplotlib.sphinxext.plot_directive import _parse_srcset
    
    # Test basic functionality
    result = _parse_srcset(["2.0x", "1.5x"])
    expected = {2.0: "2.0x", 1.5: "1.5x"}
    assert result == expected


if __name__ == "__main__":
    # Simple manual execution for debugging
    print("Testing current state...")
    
    try:
        test_plot_directive_has_srcset_config()
        print("✓ plot_srcset config test passed")
    except Exception as e:
        print(f"✗ plot_srcset config test failed: {e}")
        
    try:
        test_figure_mpl_directive_module_exists()
        print("✓ figure-mpl directive test passed")
    except Exception as e:
        print(f"✗ figure-mpl directive test failed: {e}")
        
    try:
        test_plot_directive_has_template_constants()
        print("✓ template constants test passed")
    except Exception as e:
        print(f"✗ template constants test failed: {e}")
        
    try:
        test_parse_srcset_function_exists()
        print("✓ parse srcset test passed")
    except Exception as e:
        print(f"✗ parse srcset test failed: {e}")