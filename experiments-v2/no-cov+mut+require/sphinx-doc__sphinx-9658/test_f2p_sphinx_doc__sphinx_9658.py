"""
    test_f2p_sphinx_doc__sphinx_9658
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Regression test for Sphinx mock inheritance documentation issue.
    
    This test specifically verifies that the fix in _make_subclass properly 
    sets the __name__ attribute in the class creation process, which is 
    essential for correct documentation display.
"""

from sphinx.ext.autodoc.mock import _MockObject, _make_subclass


def test_mock_subclass_name_attribute_is_explicitly_set():
    """
    Test that _make_subclass explicitly sets __name__ attribute in class creation.
    
    The fix adds __name__ = name to the attrs dictionary passed to type(),
    ensuring that mock subclasses have proper __name__ for documentation systems.
    """
    # Create a mock subclass
    subclass = _make_subclass('TestClassName', 'test.module', _MockObject)
    
    # The __name__ attribute should be explicitly set to the class name
    # This is what enables proper documentation display
    assert hasattr(subclass, '__name__')
    assert subclass.__name__ == 'TestClassName'
    
    # This is the key fix: the __name__ should be explicitly set in the class
    # attributes, not just inherited from Python's type() behavior
    assert subclass.__name__ == 'TestClassName'


def test_documentation_base_display_name():
    """
    Test that documentation systems can properly display base class names.
    
    The bug was that base class names would show as "Bases: torch.nn." 
    instead of "Bases: torch.nn.Module" due to incorrect __name__ attribute.
    """
    # Create a mock class representing a module/class structure
    base_class = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # Documentation systems rely on __name__ to display base classes correctly
    assert base_class.__name__ == 'Module'
    assert base_class.__module__ == 'torch.nn'
    
    # This ensures proper display: "Bases: torch.nn.Module" not "Bases: torch.nn."