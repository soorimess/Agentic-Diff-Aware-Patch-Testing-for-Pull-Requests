"""
Regression test for sphinx-doc/sphinx#9658
Tests that the fix prevents truncated documentation names in mocked class inheritance.
"""

from sphinx.ext.autodoc.mock import _MockObject


def test_inheritance_qualname_prevents_truncation():
    """
    Core test for the sphinx#9658 bug fix.
    
    The bug: When classes inherited from mocked classes, documentation systems 
    would show truncated names like "torch.nn." instead of "torch.nn.Module"
    
    The fix: Ensure __qualname__ is not empty to prevent truncation
    
    This test verifies that the __qualname__ attribute is properly set 
    when classes inherit from mocked classes.
    """
    # Create a mock object that simulates a module path
    mock_obj = _MockObject()
    
    # This inheritance creates the scenario described in the bug report
    class TestClass(mock_obj.SomeClass):
        pass
    
    # Get the base class that was created through inheritance
    base_class = TestClass.__bases__[0]
    
    # The critical assertion: __qualname__ should not be empty
    # This prevents documentation systems from showing truncated names
    qualname = base_class.__qualname__
    
    # Before fix: qualname would be empty string ""
    # After fix: qualname should be "SomeClass"
    assert qualname != "", (
        "Base class __qualname__ must not be empty to prevent documentation truncation. "
        "Empty qualname would cause display issues like 'torch.nn.' instead of 'torch.nn.Module'"
    )
    
    # Verify the qualname is correct
    assert qualname == "SomeClass", (
        f"Expected qualname 'SomeClass', but got '{qualname}'"
    )


def test_documentation_system_name_resolution():
    """
    Test that simulates how documentation systems resolve names.
    
    This test directly addresses the scenario from the bug report:
    - Documentation systems use __qualname__ to build display names
    - Empty __qualname__ caused truncated display 
    - Fixed __qualname__ prevents this truncation
    """
    # Simulate the torch.nn.Module scenario from the bug report
    mock_nn = _MockObject()
    mock_nn.__display_name__ = 'torch.nn'
    
    # Create a class inheriting from mocked torch.nn.Module
    class DeepKernel(mock_nn.Module):
        pass
    
    # Documentation systems would use this for display in "Bases" section
    base_class = DeepKernel.__bases__[0]
    display_name = base_class.__qualname__
    
    # This should not be empty to prevent truncated display
    assert display_name != "", (
        "Documentation display name should not be empty. "
        "Empty qualname would cause truncated display like 'torch.nn.'"
    )
    
    # Should be the full class name for correct documentation
    assert display_name == "Module", (
        f"Expected display name 'Module', but got '{display_name}'"
    )


def test_mocked_class_attributes_properly_set():
    """
    Test that the specific fix in _make_subclass is working correctly.
    
    The fix added: __name__ = name to attrs in _make_subclass
    This ensures proper attribute setting for documentation purposes.
    """
    from sphinx.ext.autodoc.mock import _make_subclass
    
    # Create a mocked class through the _make_subclass mechanism
    mocked_class = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # Both __name__ and __qualname__ should be properly set
    assert hasattr(mocked_class, '__name__'), "Mocked class should have __name__"
    assert mocked_class.__name__ == "Module", "Mocked class __name__ should be 'Module'"
    
    assert hasattr(mocked_class, '__qualname__'), "Mocked class should have __qualname__"
    assert mocked_class.__qualname__ == "Module", "Mocked class __qualname__ should be 'Module'"
    
    # The key: both should not be empty to prevent documentation issues
    assert mocked_class.__name__ != "", "Mocked class __name__ should not be empty"
    assert mocked_class.__qualname__ != "", "Mocked class __qualname__ should not be empty"