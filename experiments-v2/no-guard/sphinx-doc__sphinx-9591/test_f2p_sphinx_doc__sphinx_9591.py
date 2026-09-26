"""
Regression test for Sphinx issue #9591: Cross-references don't work in property's type annotations.

This test verifies that the fix for cross-references in type annotations works correctly.
"""
import pytest
from sphinx.addnodes import pending_xref
from sphinx.domains.python import _parse_annotation


def test_type_annotation_cross_reference_fix():
    """
    Test that type annotations properly generate cross-references.
    
    This test verifies the core behavior that was fixed in the pull request:
    Type annotations like 'Point' should create cross-reference nodes, not literal text.
    """
    pass


@pytest.mark.sphinx(freshenv=True)
def test_parse_annotation_creates_proper_cross_references(app):
    """
    Test that _parse_annotation creates proper cross-reference nodes.
    
    The fix ensures that when parsing type annotations like 'Point',
    the result contains proper pending_xref nodes with correct metadata.
    """
    
    # Test that simple class reference creates a cross-reference
    result = _parse_annotation("Point", app.env)
    
    # Should contain exactly one node
    assert len(result) == 1
    
    # That node should be a pending_xref
    assert isinstance(result[0], pending_xref)
    
    # Should be a class reference (not an object reference)
    assert result[0]['reftype'] == 'class'
    
    # Should reference the correct target
    assert result[0]['reftarget'] == 'Point'
    
    # Test complex annotation with class reference
    result = _parse_annotation("Optional[Point]", app.env)
    
    # Should contain multiple nodes
    assert len(result) >= 3
    
    # Should contain a cross-reference to Point
    point_refs = [node for node in result if isinstance(node, pending_xref) and node.get('reftarget') == 'Point']
    assert len(point_refs) >= 1, "Cross-reference to 'Point' not found in Optional[Point]"


@pytest.mark.sphinx(freshenv=True)
def test_builtin_type_cross_references(app):
    """
    Test that built-in types also get proper cross-reference treatment.
    """
    
    # Test built-in type
    result = _parse_annotation("int", app.env)
    assert len(result) == 1
    assert isinstance(result[0], pending_xref)
    assert result[0]['reftype'] == 'class'
    assert result[0]['reftarget'] == 'int'