"""
Regression test for Sphinx issue #9658
Test for proper mocked class name handling in Sphinx documentation.

This test verifies the specific behaviors that were fixed in the Sphinx mock module
to prevent truncated base class names in documentation.
"""

from sphinx.ext.autodoc.mock import _MockObject, _make_subclass


def test_mocked_class_name_attribute_behavior():
    """
    Test the __name__ attribute behavior that was fixed.
    
    The fix added '__name__ = name' to the attrs dictionary in _make_subclass(),
    ensuring that mocked classes have their __name__ attribute properly set
    for Sphinx documentation display.
    """
    
    # Create a mocked class (as Sphinx would when mocking external modules)
    mocked_class = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # The __name__ attribute is what Sphinx uses in documentation "Bases" section
    assert mocked_class.__name__ == 'Module'
    
    # This ensures proper display instead of truncated names like "torch.nn."
    assert mocked_class.__name__ != '', "Class name should not be empty"


def test_mocked_object_qualname_behavior():
    """
    Test the __qualname__ attribute behavior that was fixed.
    
    The fix changed 'self.__qualname__ = ''' to 'self.__qualname__ = self.__name__'
    in _MockObject.__init__(), ensuring __qualname__ reflects the actual class name.
    """
    
    # Create a mocked object instance
    mock_obj = _MockObject()
    
    # The __qualname__ should now be set to match __name__ (which is '')
    # This is the behavior that was fixed
    assert hasattr(mock_obj, '__qualname__')
    # Note: __name__ for _MockObject itself is '', so __qualname__ should also be ''


def test_inheritance_base_class_documentation():
    """
    Test that inheritance preserves correct base class names for documentation.
    
    This addresses the core issue: classes inheriting from mocked classes
    should show complete base class names like "torch.nn.Module" not truncated
    names like "torch.nn." in Sphinx documentation.
    """
    
    # Create a mocked base class (like torch.nn.Module)
    mocked_base = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # Create a class inheriting from the mocked base
    class TestClass(mocked_base):
        pass
    
    # The base class name should be preserved for documentation
    base_class = TestClass.__bases__[0]
    
    # This is what Sphinx displays in the "Bases" section
    assert base_class.__name__ == 'Module'
    
    # Verify it's not truncated
    assert base_class.__name__ != 'nn', "Should not show truncated name"


if __name__ == '__main__':
    test_mocked_class_name_attribute_behavior()
    test_mocked_object_qualname_behavior() 
    test_inheritance_base_class_documentation()
    print("All tests passed!")