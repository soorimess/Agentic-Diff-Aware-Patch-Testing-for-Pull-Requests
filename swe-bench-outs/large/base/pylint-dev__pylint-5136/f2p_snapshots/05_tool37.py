"""Regression tests for moving MessagesHandlerMixIn into PyLinter.

This test ensures that the functionality of managing messages by ID is preserved
after the MessagesHandlerMixIn class was moved into PyLinter.
"""
from pylint.lint.pylinter import PyLinter


def test_messages_handler_mix_in_removed_from_inheritance():
    """Test that MessagesHandlerMixIn is no longer in PyLinter's inheritance chain."""
    # Before the change, MessagesHandlerMixIn was in the MRO
    # After the change, it should not be there anymore
    mro_classes = [cls.__name__ for cls in PyLinter.__mro__]
    assert 'MessagesHandlerMixIn' not in mro_classes


def test_by_id_managed_msgs_is_instance_variable():
    """Test that by_id_managed_msgs is now an instance variable, not class variable."""
    # Create a linter instance
    linter1 = PyLinter()
    linter2 = PyLinter()
    
    # Both instances should have the attribute
    assert hasattr(linter1, '_by_id_managed_msgs')
    assert hasattr(linter2, '_by_id_managed_msgs')
    
    # Both should be lists
    assert isinstance(linter1._by_id_managed_msgs, list)
    assert isinstance(linter2._by_id_managed_msgs, list)
    
    # They should be independent instances
    assert linter1._by_id_managed_msgs is not linter2._by_id_managed_msgs
    
    # Should be properly initialized
    assert linter1._by_id_managed_msgs == []
    assert linter2._by_id_managed_msgs == []


def test_message_management_methods_on_pylinter():
    """Test that core message management methods exist directly on PyLinter."""
    linter = PyLinter()
    
    # These methods were moved from MessagesHandlerMixIn to PyLinter
    methods_to_check = [
        'disable',
        'enable', 
        'disable_next',
        '_set_msg_status',
        '_register_by_id_managed_msg',
        '_set_one_msg_status',
        '_message_symbol'
    ]
    
    for method_name in methods_to_check:
        assert hasattr(linter, method_name), f"Method {method_name} should exist on PyLinter"


def test_class_methods_removed():
    """Test that MessagesHandlerMixIn class methods are no longer accessible on PyLinter."""
    # These were class methods in MessagesHandlerMixIn that should not exist on PyLinter anymore
    assert not hasattr(PyLinter, 'clear_by_id_managed_msgs')
    assert not hasattr(PyLinter, 'get_by_id_managed_msgs')