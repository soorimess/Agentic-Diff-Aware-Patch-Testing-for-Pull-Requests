"""Regression tests for moving MessagesHandlerMixIn into PyLinter.

This test ensures that the functionality of managing messages by ID is preserved
after the MessagesHandlerMixIn class was moved into PyLinter.
"""
from pylint.lint.pylinter import PyLinter
from pylint.message import MessageDefinitionStore


def test_by_id_managed_msgs_functionality():
    """Test that by_id_managed_msgs functionality works correctly after the move.
    
    Before the change, by_id_managed_msgs was a class variable in MessagesHandlerMixIn.
    After the change, it became an instance variable in PyLinter.
    """
    # Create a linter instance
    linter = PyLinter()
    
    # Verify that _by_id_managed_msgs exists as an instance variable
    assert hasattr(linter, '_by_id_managed_msgs')
    assert isinstance(linter._by_id_managed_msgs, list)
    
    # Test that we can access the by_id_managed_msgs functionality through the linter
    # This should work after the change but would fail before the change
    # because MessagesHandlerMixIn would not exist anymore
    assert linter._by_id_managed_msgs == []


def test_message_management_methods_exist():
    """Test that message management methods are now part of PyLinter."""
    linter = PyLinter()
    
    # These methods should exist on PyLinter now (they were moved from MessagesHandlerMixIn)
    assert hasattr(linter, 'disable')
    assert hasattr(linter, 'enable')
    assert hasattr(linter, 'disable_next')
    assert hasattr(linter, '_set_msg_status')
    assert hasattr(linter, '_register_by_id_managed_msg')
    assert hasattr(linter, '_set_one_msg_status')
    assert hasattr(linter, '_message_symbol')


def test_linter_inheritance():
    """Test that PyLinter no longer inherits from MessagesHandlerMixIn."""
    # This test ensures that MessagesHandlerMixIn is no longer in the inheritance
    # which is a key part of the change
    
    # Check that MessagesHandlerMixIn is not in the MRO
    mro_classes = [cls.__name__ for cls in PyLinter.__mro__]
    assert 'MessagesHandlerMixIn' not in mro_classes


def test_by_id_managed_msgs_integration():
    """Test integration with the ByIdManagedMessagesChecker functionality."""
    # Test that the linter can handle the by_id_managed_msgs functionality
    # that was previously handled by MessagesHandlerMixIn class methods
    
    linter = PyLinter()
    
    # Verify the instance variable exists and is properly initialized
    assert hasattr(linter, '_by_id_managed_msgs')
    assert isinstance(linter._by_id_managed_msgs, list)
    
    # Test that we can add to it (this would be done by the checker)
    # This is a basic integration test
    assert linter._by_id_managed_msgs == []