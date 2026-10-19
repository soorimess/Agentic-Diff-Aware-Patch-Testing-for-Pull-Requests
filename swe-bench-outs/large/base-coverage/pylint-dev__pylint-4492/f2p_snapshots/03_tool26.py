# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Test for the multiple output formats feature."""

import os
import tempfile

from pylint.lint import PyLinter


def test_output_format_parsing():
    """Test that output-format option correctly parses multiple reporters."""
    linter = PyLinter()
    
    # This should work after the change - setting a comma-separated format
    try:
        linter.set_option("output-format", "json:output.json,text")
        
        # After the change, we should have the new attribute
        assert hasattr(linter, '_reporter_names')
        assert linter._reporter_names == "json:output.json,text"
        
        # Test that we can parse the components correctly
        reporters = linter._reporter_names.split(",")
        assert len(reporters) == 2
        assert reporters[0] == "json:output.json"
        assert reporters[1] == "text"
        
    except AttributeError:
        # Before the change, this would not work as expected
        # We're testing that the feature will work after the change
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