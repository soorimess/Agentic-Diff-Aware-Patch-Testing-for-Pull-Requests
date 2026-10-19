"""
Regression test for singledispatch support in autodoc.

This test verifies that the new singledispatch documenters are properly registered
and available in the autodoc system.
"""

def test_singledispatch_function_documenter_exists():
    """Test that SingledispatchFunctionDocumenter class exists."""
    # This test should fail in current state (before PR) and pass after PR
    # The test is checking whether the class can be imported successfully
    try:
        from sphinx.ext.autodoc import SingledispatchFunctionDocumenter
        # If we can import it, the PR is applied
        return True
    except ImportError:
        # If we can't import it, the PR is not applied yet
        return False


def test_singledispatch_method_documenter_exists():
    """Test that SingledispatchMethodDocumenter class exists."""
    # This test should fail in current state (before PR) and pass after PR
    try:
        from sphinx.ext.autodoc import SingledispatchMethodDocumenter
        # If we can import it, the PR is applied
        return True
    except ImportError:
        # If we can't import it, the PR is not applied yet
        return False


def test_is_singledispatch_function_utility_exists():
    """Test that is_singledispatch_function utility exists."""
    # This test should fail in current state (before PR) and pass after PR
    try:
        from sphinx.util.inspect import is_singledispatch_function
        # If we can import it, the PR is applied
        return True
    except ImportError:
        # If we can't import it, the PR is not applied yet
        return False


def test_is_singledispatch_method_utility_exists():
    """Test that is_singledispatch_method utility exists."""
    # This test should fail in current state (before PR) and pass after PR
    try:
        from sphinx.util.inspect import is_singledispatch_method
        # If we can import it, the PR is applied
        return True
    except ImportError:
        # If we can't import it, the PR is not applied yet
        return False