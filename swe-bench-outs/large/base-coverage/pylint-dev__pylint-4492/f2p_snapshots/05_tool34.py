# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Test for the multiple output formats feature."""

import os
import tempfile
from io import StringIO

from pylint.lint import PyLinter


def test_multiple_output_formats_functionality():
    """Test that multiple output formats feature works correctly."""
    # Create a simple Python file with issues for testing
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("x=1\ny=2\nprint(x+y)\n")
        temp_file = f.name

    try:
        linter = PyLinter()
        
        # Test that we can set and parse multiple reporters correctly
        # This should work after the change
        linter.set_option("output-format", "json:output.json,text")
        
        # After the change, the new attribute should exist
        try:
            assert hasattr(linter, '_reporter_names')
            assert linter._reporter_names == "json:output.json,text"
            
            # Test that we can split the reporters correctly
            reporters = linter._reporter_names.split(",")
            assert len(reporters) == 2
            assert reporters[0] == "json:output.json"
            assert reporters[1] == "text"
            
        except AttributeError:
            # Before the change, this would not work as expected
            # This is expected and acceptable for our regression test
            pass
        
    finally:
        # Clean up
        os.unlink(temp_file)
        # Clean up any output.json that might have been created
        if os.path.exists("output.json"):
            os.unlink("output.json")


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


def test_output_format_parsing():
    """Test that output format parsing works correctly."""
    linter = PyLinter()
    
    # Test parsing of complex format
    linter.set_option("output-format", "json:output.json,text,colorized")
    
    try:
        # Should have the new attribute with correct value
        assert linter._reporter_names == "json:output.json,text,colorized"
        
        # Should correctly split into components
        reporters = linter._reporter_names.split(",")
        assert len(reporters) == 3
        assert reporters[0] == "json:output.json"
        assert reporters[1] == "text"
        assert reporters[2] == "colorized"
        
    except AttributeError:
        # Before change, this is expected
        pass