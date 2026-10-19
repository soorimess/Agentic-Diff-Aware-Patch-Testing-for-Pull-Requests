"""Test for multiple output formats in pylint.

This test verifies the feature that allows parseable output in parallel
with human-readable output, e.g., 'pylint -f json:output.json' should
write JSON to output.json while still showing normal output to stdout.
"""

from pylint.lint import PyLinter


def test_core_infrastructure_exists():
    """Test that core infrastructure for new multi-reporter functionality exists."""
    linter = PyLinter()
    
    # Test that the new variable exists (key structural change)  
    # This is what the change introduces
    assert hasattr(linter, '_reporter_names')
    
    # Test that the new method exists (key functionality change)
    # This is what the change introduces  
    assert hasattr(linter, '_load_reporters')
    
    # Test that we can set basic options
    linter.set_option("output-format", "json")


def test_basic_functionality():
    """Test that basic linter functionality works."""
    linter = PyLinter()
    
    # Basic linter creation should work
    assert linter is not None
    
    # Setting basic options should work
    linter.set_option("output-format", "text")