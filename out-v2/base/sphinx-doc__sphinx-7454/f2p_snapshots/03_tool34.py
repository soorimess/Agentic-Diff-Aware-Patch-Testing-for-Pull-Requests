"""
Regression test for inconsistent handling of None by autodoc_typehints.

This test verifies that None type hints are consistently treated as object
references regardless of autodoc_typehints mode.
"""
from sphinx.domains.python import _parse_annotation
from sphinx.addnodes import pending_xref


def test_parse_annotation_none_reftype():
    """Test that _parse_annotation correctly handles 'None' type annotation."""
    # Test that 'None' annotation produces a pending_xref with reftype='obj'
    result = _parse_annotation('None')
    
    # Should return a list with one element
    assert len(result) == 1
    node = result[0]
    
    # Should be a pending_xref node
    assert isinstance(node, pending_xref)
    
    # The reftype should be 'obj' for None, not 'class'
    assert node.get('reftype') == 'obj'


def test_parse_annotation_int_reftype():
    """Test that non-None type annotations still work correctly."""
    # Test that 'int' annotation produces a pending_xref with reftype='class'
    result = _parse_annotation('int')
    
    # Should return a list with one element
    assert len(result) == 1
    node = result[0]
    
    # Should be a pending_xref node
    assert isinstance(node, pending_xref)
    
    # The reftype should be 'class' for int
    assert node.get('reftype') == 'class'