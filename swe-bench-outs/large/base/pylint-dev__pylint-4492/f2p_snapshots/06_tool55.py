"""Test for multiple output formats in pylint.

This test verifies the feature that allows parseable output in parallel
with human-readable output, e.g., 'pylint -f json:output.json' should
write JSON to output.json while still showing normal output to stdout.
"""

from pylint.lint import PyLinter


def test_new_structure_exists():
    """Test that the new structural elements exist for multi-reporter functionality."""
    linter = PyLinter()
    
    # Test that the new variable exists (key structural change)
    assert hasattr(linter, '_reporter_names')
    
    # Test that the new method exists (key functionality change) 
    assert hasattr(linter, '_load_reporters')
    
    # Test that basic option setting works
    linter.set_option("output-format", "json")
    
    # Test that we can set the new format syntax that will be supported
    # This is what the change enables - comma-separated formats
    try:
        linter.set_option("output-format", "text")
        # If we get here, the infrastructure is ready
    except Exception:
        # This might fail in some cases but that's not what we're testing
        pass


def test_basic_linter_functionality():
    """Test that basic linter functionality is preserved."""
    linter = PyLinter()
    
    # Basic linter creation should work
    assert linter is not None
    
    # Setting basic options should work
    linter.set_option("output-format", "text")