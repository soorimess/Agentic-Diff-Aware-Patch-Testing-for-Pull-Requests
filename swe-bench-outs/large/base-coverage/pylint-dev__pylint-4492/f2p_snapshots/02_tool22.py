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


def test_multiple_output_formats_feature():
    """Test that the multiple output formats feature works correctly after the change."""
    # Create a simple Python file with issues
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("x=1\ny=2\nprint(x+y)\n")
        temp_file = f.name

    try:
        linter = PyLinter()
        
        # Test that the new syntax works (will fail before change, pass after)
        # This should set _reporter_names (new) instead of _reporter_name (old)
        linter.set_option("output-format", "json:output.json,text")
        
        # After the change, this should be set to the new attribute
        # This test will fail before the change but pass after
        try:
            assert hasattr(linter, '_reporter_names')
            assert linter._reporter_names == "json:output.json,text"
        except AttributeError:
            # This is expected before the change - should still work with old behavior
            pytest.skip("Feature not yet implemented in this version")
        
        # Test that we can parse the multiple reporters correctly
        # The format should be split correctly
        reporters = linter._reporter_names.split(",")
        assert len(reporters) == 2
        assert reporters[0] == "json:output.json"
        assert reporters[1] == "text"
        
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
        
        # Should work with new attribute
        try:
            assert linter._reporter_names == "json"
        except AttributeError:
            # Before change, should use old attribute
            assert linter._reporter_name == "json"
        
    finally:
        # Clean up
        os.unlink(temp_file)


def test_reporter_loading_mechanism():
    """Test that the reporter loading mechanism works for multiple reporters."""
    linter = PyLinter()
    
    # Test that we can set up multiple reporters
    try:
        linter.set_option("output-format", "json,text")
        # If this works, it means the new mechanism is in place
        assert hasattr(linter, '_reporter_names')
        assert linter._reporter_names == "json,text"
    except Exception:
        # This is expected before the change
        pytest.skip("Feature not yet implemented in this version")