"""Regression tests for the MessagesHandlerMixIn to PyLinter merge.

This test ensures that the functionality related to managing messages by ID
is properly working after the refactoring.
"""

import pytest
from pylint.lint.pylinter import PyLinter


def test_messages_handler_mix_in_removed():
    """Test that MessagesHandlerMixIn is no longer available in the message module."""
    # In the new version, MessagesHandlerMixIn should not be importable
    # This test will fail in the old version but pass in the new version
    try:
        from pylint.message import MessagesHandlerMixIn
        # If we get here, it means MessagesHandlerMixIn still exists (old version)
        # This test should pass in the new version where it's removed
        assert False, "MessagesHandlerMixIn should not exist in new version"
    except ImportError:
        # This is expected in the new version
        pass


def test_linter_inheritance_change():
    """Test that PyLinter no longer inherits from MessagesHandlerMixIn."""
    # In the old version, PyLinter would inherit from MessagesHandlerMixIn
    # In the new version, it should not
    try:
        from pylint.message import MessagesHandlerMixIn
        # Check if MessagesHandlerMixIn is in the MRO
        mro_classes = [cls.__name__ for cls in PyLinter.__mro__]
        # This should be False in the new version
        assert "MessagesHandlerMixIn" not in mro_classes
    except ImportError:
        # If MessagesHandlerMixIn doesn't exist, we're in the new version
        # This is the expected behavior
        pass


def test_message_management_methods_on_linter():
    """Test that message management methods are now on PyLinter instance."""
    linter = PyLinter()
    
    # These methods should exist on the PyLinter instance in the new version
    # They were moved from MessagesHandlerMixIn to PyLinter
    methods_to_check = [
        'disable',
        'enable', 
        'disable_next',
        '_set_msg_status',
        '_register_by_id_managed_msg',
        '_message_symbol',
        '_set_one_msg_status'
    ]
    
    for method_name in methods_to_check:
        # These should exist on the linter instance
        assert hasattr(linter, method_name), f"Method {method_name} should exist on PyLinter"


def test_by_id_managed_msgs_functionality():
    """Test that the by_id_managed_msgs functionality works correctly."""
    # Create a linter instance
    linter = PyLinter()
    
    # Check that _by_id_managed_msgs attribute exists (this was added in the new version)
    # In the old version, this attribute would not exist yet
    assert hasattr(linter, '_by_id_managed_msgs')
    
    # Check that it's initialized as an empty list
    assert linter._by_id_managed_msgs == []
    
    # Test that we can add items to it (this tests the instance variable behavior)
    linter._by_id_managed_msgs.append(("test_module", "C0001", "test-message", 10, True))
    assert len(linter._by_id_managed_msgs) == 1


def test_message_symbol_method_behavior():
    """Test that _message_symbol method behaves correctly."""
    linter = PyLinter()
    
    # Test that the method can be called without crashing
    # This tests that the method logic isn't completely broken
    # We don't need to test exact return values, just that it doesn't crash
    result = linter._message_symbol("C0001")
    # Should return a list
    assert isinstance(result, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])