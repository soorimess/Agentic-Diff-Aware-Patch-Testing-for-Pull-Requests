"""
Regression test for sphinx-doc/sphinx#9658

This test ensures that Sphinx documentation generation for classes inheriting 
from mocked classes behaves correctly, avoiding truncated base class names.

The fix ensures __qualname__ is set appropriately so that base class display
shows complete names like "torch.nn.Module" instead of truncated "torch.nn."
"""
from sphinx.ext.autodoc.mock import _MockObject, _make_subclass


def test_mocked_class_inheritance_display():
    """
    Test that verifies the behavior change regarding inheritance display.
    
    Previously, when Sphinx documentation tried to display classes that 
    inherit from mocked classes, it would show truncated base names like:
        "Bases: torch.nn."
    instead of 
        "Bases: torch.nn.Module"
    
    This happened because the qualname was incorrectly set or empty.
    """
    
    # Create a mock that represents a real class like torch.nn.Module  
    # This simulates what a mocked parent class would look like
    mock_parent = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # Verify the fix: qualname should not be empty, or the display would be truncated
    assert mock_parent.__qualname__ != '', (
        "If __qualname__ were empty, Sphinx would display truncated bases "
        "like 'torch.nn.' instead of 'torch.nn.Module'"
    )
    
    # Test that the qualified display works correctly
    # This is how Sphinx constructs the display string: __module__ + '.' + __qualname__
    bases_display = f"{mock_parent.__module__}.{mock_parent.__qualname__}"
    
    # The bug was that instead of "torch.nn.Module", Sphinx would show "torch.nn."
    # which is incomplete and wrong
    assert bases_display == 'torch.nn.Module', (
        "Sphinx documentation should show complete base class name, not truncated form"
    )
    
    # Verify structural attributes are properly set
    assert mock_parent.__name__ == 'Module'
    assert mock_parent.__qualname__ == 'Module' 
    assert mock_parent.__module__ == 'torch.nn'


def test_no_truncated_base_display():
    """
    Explicit test that catches the specific bug scenario:
    Before fix - __qualname__ was '' or incorrectly derived leading to truncation
    After fix - __qualname__ properly reflects full class name
    """
    
    # Create a mock that would represent something like torch.nn.Module
    torch_nn_module = _make_subclass('Module', 'torch.nn', _MockObject) 
    
    # The key validation: truncated display happens when qualname is bad
    # This test will catch if qualname is set to something that results in truncation  
    full_name = torch_nn_module.__module__ + '.' + torch_nn_module.__qualname__
    
    # The test fails if we produce truncated output like "torch.nn."
    # which is the bug described in the issue
    assert not full_name.endswith('.'), (
        "Base class display should not end with dot (indicating truncation). "
        "This was the core bug: showing 'torch.nn.' instead of 'torch.nn.Module'"
    )
    
    # The expected correct output
    assert full_name == 'torch.nn.Module'