"""Regression tests for moving MessagesHandlerMixIn into PyLinter.

This test ensures that the functionality of managing messages by ID is preserved
after the MessagesHandlerMixIn class was moved into PyLinter.
"""
from pylint.lint.pylinter import PyLinter


def test_linter_inheritance_change():
    """Test that MessagesHandlerMixIn is no longer in PyLinter's inheritance."""
    # This is the core change: MessagesHandlerMixIn should no longer be in the MRO
    mro_classes = [cls.__name__ for cls in PyLinter.__mro__]
    assert 'MessagesHandlerMixIn' not in mro_classes


def test_by_id_managed_msgs_instance_variable():
    """Test that _by_id_managed_msgs is now an instance variable of PyLinter."""
    # Create a linter instance
    linter = PyLinter()
    
    # Verify that _by_id_managed_msgs exists as an instance variable
    assert hasattr(linter, '_by_id_managed_msgs')
    assert isinstance(linter._by_id_managed_msgs, list)
    
    # Test that it's properly initialized
    assert linter._by_id_managed_msgs == []


def test_message_management_methods_exist():
    """Test that core message management methods exist on PyLinter."""
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


def test_no_class_methods_from_messages_handler_mix_in():
    """Test that class methods from MessagesHandlerMixIn are no longer accessible."""
    # Before the change, these were class methods:
    # MessagesHandlerMixIn.clear_by_id_managed_msgs
    # MessagesHandlerMixIn.get_by_id_managed_msgs
    
    # These should not exist anymore
    assert not hasattr(PyLinter, 'clear_by_id_managed_msgs')
    assert not hasattr(PyLinter, 'get_by_id_managed_msgs')