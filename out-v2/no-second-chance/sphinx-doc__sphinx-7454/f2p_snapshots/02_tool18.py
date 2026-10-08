"""Regression test for inconsistent handling of None by autodoc_typehints.

This test ensures that None in type hints links to the documentation for the
None singleton regardless of whether 'description' or 'signature' mode is used.
"""

from sphinx.domains.python import _parse_annotation
from sphinx.domains import python as pydomain
from sphinx.addnodes import pending_xref
from sphinx.util.docutils import docutils_namespace


def test_parse_annotation_none_handling():
    """Test that _parse_annotation handles 'None' specially with reftype='obj'."""
    # Test the current (buggy) behavior
    result = _parse_annotation("None")
    
    # The result should be a pending_xref node
    assert len(result) == 1
    node = result[0]
    assert isinstance(node, pending_xref)
    
    # Before the fix, this would be 'class' - after the fix it should be 'obj'
    # This test will fail before the fix and pass after the fix
    expected_reftype = 'obj'  # This is what the fix makes it
    actual_reftype = node.get('reftype', 'class')  # Default to 'class' for old behavior
    
    # The fix ensures that 'None' gets reftype='obj' instead of 'class'
    # This is the key difference we're testing
    assert actual_reftype == expected_reftype, f"Expected reftype='obj' for None, got '{actual_reftype}'"


def test_parse_annotation_regular_types():
    """Test that regular types still work correctly."""
    # Test regular type annotation
    result = _parse_annotation("int")
    
    # The result should be a pending_xref node
    assert len(result) == 1
    node = result[0]
    assert isinstance(node, pending_xref)
    
    # Regular types should still use 'class' reftype
    expected_reftype = 'class'
    actual_reftype = node.get('reftype', 'class')
    assert actual_reftype == expected_reftype


def test_parse_annotation_none_vs_regular():
    """Test the difference between None and regular types."""
    none_result = _parse_annotation("None")
    int_result = _parse_annotation("int")
    
    # Both should be pending_xref nodes
    assert len(none_result) == 1
    assert len(int_result) == 1
    
    none_node = none_result[0]
    int_node = int_result[0]
    
    assert isinstance(none_node, pending_xref)
    assert isinstance(int_node, pending_xref)
    
    # The key difference: None should have reftype='obj', int should have reftype='class'
    none_reftype = none_node.get('reftype', 'class')
    int_reftype = int_node.get('reftype', 'class')
    
    # Before fix: both would be 'class'
    # After fix: None should be 'obj', int should be 'class'
    assert none_reftype == 'obj', f"None should have reftype='obj', got '{none_reftype}'"
    assert int_reftype == 'class', f"int should have reftype='class', got '{int_reftype}'"