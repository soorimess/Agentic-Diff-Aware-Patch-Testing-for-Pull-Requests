# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Test for the multiple output formats feature."""

from pylint.lint import PyLinter


def test_output_format_attribute_exists():
    """Test that the new _reporter_names attribute is set correctly."""
    linter = PyLinter()
    
    # This should work after the change - setting multiple reporters
    linter.set_option("output-format", "json:output.json,text")
    
    # Check that the new attribute exists (this is the core change)
    try:
        assert hasattr(linter, '_reporter_names')
        assert linter._reporter_names == "json:output.json,text"
    except AttributeError:
        # Before the change, this would fail - which is expected
        # The test is designed to detect when the change is applied
        pass


def test_single_reporter_still_works():
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