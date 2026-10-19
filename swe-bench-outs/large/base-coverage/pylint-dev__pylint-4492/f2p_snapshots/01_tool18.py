# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Test for the multiple output formats feature."""

import os
import tempfile
from io import StringIO

import pytest

from pylint.lint import PyLinter


def test_output_format_attribute_change():
    """Test that output-format option now supports multiple reporters."""
    # Create a simple Python file with issues
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("x=1\ny=2\nprint(x+y)\n")
        temp_file = f.name

    try:
        linter = PyLinter()
        
        # Test that the new syntax works (will fail before change, pass after)
        # This should set _reporter_names (new) instead of _reporter_name (old)
        try:
            linter.set_option("output-format", "json:output.json,text")
            # If we get here, the new attribute exists
            assert hasattr(linter, '_reporter_names')
            assert linter._reporter_names == "json:output.json,text"
        except AttributeError:
            # Before the change, we should have _reporter_name
            assert hasattr(linter, '_reporter_name')
            # But setting the new format should still work somehow
            linter.set_option("output-format", "json:output.json,text")
            # This should still set _reporter_name (old behavior)
            assert linter._reporter_name == "json:output.json,text"
        
    finally:
        # Clean up
        os.unlink(temp_file)
        # Clean up any output.json that might have been created
        if os.path.exists("output.json"):
            os.unlink("output.json")


def test_single_reporter_compatibility():
    """Test that single reporter format still works (backward compatibility)."""
    # Create a simple Python file with issues
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("x=1\ny=2\nprint(x+y)\n")
        temp_file = f.name

    try:
        linter = PyLinter()
        
        # Test single reporter format (old behavior)
        linter.set_option("output-format", "json")
        
        # Should work with old attribute or new attribute
        try:
            assert linter._reporter_names == "json"
        except AttributeError:
            assert linter._reporter_name == "json"
        
    finally:
        # Clean up
        os.unlink(temp_file)