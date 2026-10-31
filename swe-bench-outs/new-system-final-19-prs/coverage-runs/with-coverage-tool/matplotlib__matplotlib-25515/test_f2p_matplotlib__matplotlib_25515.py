"""
Test for the hi-res plot directive enhancement.

This test verifies the behavior of the new plot_srcset functionality
that allows creating responsive hi-DPI images for sphinx documentation.
"""

import pytest
from unittest.mock import MagicMock, patch
import tempfile
import os
from pathlib import Path


def test_plot_directive_setup_adds_srcset_config():
    """
    Test that plot_directive.setup properly adds plot_srcset configuration.
    
    This tests the core behavior change: the setup function now registers
    the plot_srcset config option.
    """
    from matplotlib.sphinxext.plot_directive import setup
    
    # Create a mock Sphinx app
    mock_app = MagicMock()
    
    # Call setup - this should register the plot_srcset config
    result = setup(mock_app)
    
    # Verify that add_config_value was called with the right parameters
    mock_app.add_config_value.assert_any_call('plot_srcset', [], True)
    
    # Verify the returned metadata
    assert 'parallel_read_safe' in result
    assert 'parallel_write_safe' in result
    assert 'version' in result


def test_parse_srcset_function_returns_correct_dict():
    """
    Test that _parse_srcset function correctly parses srcset entries.
    
    This tests the core functionality that was added to handle srcset parsing.
    """
    from matplotlib.sphinxext.plot_directive import _parse_srcset
    
    # Test with multiple entries
    entries = ["2.0x", "1.5x"]
    result = _parse_srcset(entries)
    expected = {2.0: "2.0x", 1.5: "1.5x"}
    assert result == expected
    
    # Test with single entry
    entries = ["2.0x"]
    result = _parse_srcset(entries)
    expected = {2.0: "2.0x"}
    assert result == expected


def test_parse_srcset_nodes_function_returns_correct_dict():
    """
    Test that _parse_srcsetNodes function correctly parses srcset strings.
    
    This tests the core functionality in figmpl_directive for parsing srcset strings.
    """
    from matplotlib.sphinxext.figmpl_directive import _parse_srcsetNodes
    
    # Test basic functionality with comma-separated entries
    srcset_str = "test.png, test.2x.png 2.00x"
    result = _parse_srcsetNodes(srcset_str)
    expected = {0: "test.png", 2.0: "test.2x.png"}
    assert result == expected
    
    # Test single entry
    srcset_str = "test.png"
    result = _parse_srcsetNodes(srcset_str)
    expected = {0: "test.png"}
    assert result == expected


def test_template_constants_exist_and_are_different():
    """
    Test that TEMPLATE_SRCSET and TEMPLATE constants exist and are different.
    
    This verifies the new template constants were added to support srcset functionality.
    """
    from matplotlib.sphinxext.plot_directive import TEMPLATE_SRCSET, TEMPLATE
    
    # Both should exist and be non-None
    assert TEMPLATE_SRCSET is not None
    assert TEMPLATE is not None
    
    # They should be different (different functionality)
    assert TEMPLATE_SRCSET != TEMPLATE


def test_figure_mpl_directive_has_correct_structure_and_run_method():
    """
    Test that FigureMpl class has the correct structure and run method.
    
    This verifies the new directive class was properly implemented with its run method.
    """
    from matplotlib.sphinxext.figmpl_directive import FigureMpl
    
    # Check key attributes exist and have expected values
    assert hasattr(FigureMpl, 'has_content')
    assert hasattr(FigureMpl, 'required_arguments') 
    assert hasattr(FigureMpl, 'optional_arguments')
    assert hasattr(FigureMpl, 'option_spec')
    assert hasattr(FigureMpl, 'run')
    
    # Check that the class is properly defined
    assert FigureMpl.has_content is False
    assert FigureMpl.required_arguments == 1
    assert FigureMpl.optional_arguments == 2
    assert 'alt' in FigureMpl.option_spec
    assert 'srcset' in FigureMpl.option_spec
    
    # Verify the run method exists and is callable
    assert callable(FigureMpl.run)
    
    # Check that it has the right signature (at least has 'self' parameter)
    import inspect
    sig = inspect.signature(FigureMpl.run)
    assert len(sig.parameters) >= 1


if __name__ == "__main__":
    # Simple manual execution for debugging
    print("Testing current state...")
    
    try:
        test_plot_directive_setup_adds_srcset_config()
        print("✓ plot directive setup test passed")
    except Exception as e:
        print(f"✗ plot directive setup test failed: {e}")
        
    try:
        test_parse_srcset_function_returns_correct_dict()
        print("✓ parse srcset test passed")
    except Exception as e:
        print(f"✗ parse srcset test failed: {e}")
        
    try:
        test_parse_srcset_nodes_function_returns_correct_dict()
        print("✓ parse srcset nodes test passed")
    except Exception as e:
        print(f"✗ parse srcset nodes test failed: {e}")
        
    try:
        test_template_constants_exist_and_are_different()
        print("✓ template constants test passed")
    except Exception as e:
        print(f"✗ template constants test failed: {e}")
        
    try:
        test_figure_mpl_directive_has_correct_structure_and_run_method()
        print("✓ figure-mpl directive structure test passed")
    except Exception as e:
        print(f"✗ figure-mpl directive structure test failed: {e}")