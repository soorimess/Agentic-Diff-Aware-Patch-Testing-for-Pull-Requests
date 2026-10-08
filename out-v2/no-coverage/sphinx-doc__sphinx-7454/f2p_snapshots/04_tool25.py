"""
Regression test for sphinx-doc/sphinx#7454

This test ensures that None type hints are consistently handled as clickable
links regardless of the autodoc_typehints setting.
"""
import pytest
from sphinx.domains.python import _parse_annotation


def test_none_typehint_parsing():
    """Test that None type hint is parsed with correct reftype."""
    
    # Test parsing of None annotation
    none_nodes = _parse_annotation('None')
    
    # Should produce a pending_xref node
    assert len(none_nodes) == 1
    node = none_nodes[0]
    
    # Check that it's a pending_xref node
    from sphinx import addnodes
    assert isinstance(node, addnodes.pending_xref)
    
    # Check the reftype - this is the key test for the bug fix
    # Before fix: reftype was 'class' for None (which doesn't link properly)
    # After fix: reftype should be 'obj' for None (which links to Python docs)
    assert node.get('reftype') == 'obj', "None type hint should use reftype='obj' for proper linking"


def test_other_typehint_parsing():
    """Test that other type hints still work correctly."""
    
    # Test parsing of int annotation  
    int_nodes = _parse_annotation('int')
    
    # Should produce a pending_xref node
    assert len(int_nodes) == 1
    node = int_nodes[0]
    
    # Check that it's a pending_xref node
    from sphinx import addnodes
    assert isinstance(node, addnodes.pending_xref)
    
    # Check the reftype - int should still use 'class' 
    assert node.get('reftype') == 'class', "int type hint should use reftype='class'"


def test_none_vs_other_typehint_consistency():
    """Test that None and other type hints are handled consistently."""
    
    # Parse both None and int
    none_nodes = _parse_annotation('None')
    int_nodes = _parse_annotation('int')
    
    # Both should be pending_xref nodes
    from sphinx import addnodes
    assert isinstance(none_nodes[0], addnodes.pending_xref)
    assert isinstance(int_nodes[0], addnodes.pending_xref)
    
    # Check their reftypes
    none_reftype = none_nodes[0].get('reftype')
    int_reftype = int_nodes[0].get('reftype')
    
    # None should use 'obj' reftype (the fix)
    assert none_reftype == 'obj', f"None should use 'obj' reftype, got '{none_reftype}'"
    
    # int should use 'class' reftype (existing behavior)
    assert int_reftype == 'class', f"int should use 'class' reftype, got '{int_reftype}'"


def test_none_typehint_has_correct_refdomain():
    """Test that None type hint has correct refdomain for proper linking."""
    
    # Test parsing of None annotation
    none_nodes = _parse_annotation('None')
    
    # Should produce a pending_xref node
    assert len(none_nodes) == 1
    node = none_nodes[0]
    
    # Check that it has the correct refdomain
    assert node.get('refdomain') == 'py', "None type hint should use refdomain='py'"


def test_none_typehint_has_correct_reftarget():
    """Test that None type hint has correct reftarget."""
    
    # Test parsing of None annotation
    none_nodes = _parse_annotation('None')
    
    # Should produce a pending_xref node
    assert len(none_nodes) == 1
    node = none_nodes[0]
    
    # Check that it has the correct reftarget
    assert node.get('reftarget') == 'None', "None type hint should have reftarget='None'"