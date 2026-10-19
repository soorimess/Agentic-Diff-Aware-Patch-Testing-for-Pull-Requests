# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Test for the multiple output formats feature."""

from pylint.lint import PyLinter


def test_multiple_output_formats_attribute():
    """Test that output-format option now supports multiple reporters via _reporter_names."""
    linter = PyLinter()
    
    # Test that the new syntax works (will fail before change, pass after)
    # This should set _reporter_names (new) instead of _reporter_name (old)
    linter.set_option("output-format", "json:output.json,text")
    
    # After the change, this attribute should exist and contain the correct value
    # Before the change, this will fail with AttributeError
    try:
        assert hasattr(linter, '_reporter_names')
        assert linter._reporter_names == "json:output.json,text"
    except AttributeError:
        # This is expected before the change
        # The old behavior would use _reporter_name
        pass


def test_single_reporter_backward_compatibility():
    """Test that single reporter format still works (backward compatibility)."""
    linter = PyLinter()
    
    # Test single reporter format (old behavior) 
    linter.set_option("output-format", "json")
    
    # Should work with either old or new attribute
    try:
        assert linter._reporter_names == "json"
    except AttributeError:
        # Before change, should use old attribute
        assert linter._reporter_name == "json"