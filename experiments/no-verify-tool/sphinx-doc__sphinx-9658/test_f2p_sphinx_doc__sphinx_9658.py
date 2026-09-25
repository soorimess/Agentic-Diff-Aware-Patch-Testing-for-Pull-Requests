"""
test_f2p_sphinx_doc__sphinx_9658
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Regression test for Sphinx bug where inherited classes are not correctly documented when mocked.

:copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from sphinx.ext.autodoc.mock import _MockObject


def test_mock_object_qualname_is_not_empty():
    """
    Test that demonstrates the bug in Sphinx 3.4.2+ where mock objects 
    used as base classes have empty __qualname__, causing documentation
    to show incomplete base class names like "Bases: torch.nn." instead 
    of "Bases: torch.nn.Module".
    
    This test will fail on buggy code and pass after the fix is applied.
    """
    # Create a mock object that represents a mocked class like torch.nn.Module
    mock_obj = _MockObject()
    
    # The bug: __qualname__ = '' (empty string) - causes incomplete display
    # The fix: __qualname__ should be properly set (not empty)
    qualname = getattr(mock_obj, '__qualname__', '')
    
    # This assertion should pass after the fix to ensure proper document rendering
    assert qualname != '', f"Mock object __qualname__ should not be empty, but got: '{qualname}'"