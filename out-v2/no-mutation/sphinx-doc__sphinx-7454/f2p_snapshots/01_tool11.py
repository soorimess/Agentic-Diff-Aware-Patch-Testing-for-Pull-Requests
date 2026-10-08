"""
Regression test for sphinx-doc/sphinx#7454

This test ensures that None type hints are consistently handled
regardless of whether autodoc_typehints is set to 'signature' or 'description'.
"""
from sphinx.domains.python import _parse_annotation
from sphinx.addnodes import pending_xref


def test_parse_annotation_none_handling():
    """Test that _parse_annotation handles 'None' with correct reftype."""
    # Test that 'None' is parsed with reftype='obj', not 'class'
    result = _parse_annotation('None')
    
    # Should contain a pending_xref node
    assert len(result) == 1
    assert isinstance(result[0], pending_xref)
    
    # The reftype should be 'obj' for None, not 'class' (this is the bug)
    xref_node = result[0]
    # This assertion should pass after the fix is applied
    assert xref_node.get('reftype') == 'obj'
    assert xref_node.get('reftarget') == 'None'


def test_parse_annotation_consistency():
    """Test that the parsing behavior is consistent for None vs other types."""
    # Test None parsing - should use 'obj' reftype
    none_result = _parse_annotation('None')
    assert len(none_result) == 1
    assert isinstance(none_result[0], pending_xref)
    assert none_result[0].get('reftype') == 'obj'  # This should be 'obj' for None
    
    # Test int parsing - should use 'class' reftype  
    int_result = _parse_annotation('int')
    assert len(int_result) == 1
    assert isinstance(int_result[0], pending_xref)
    assert int_result[0].get('reftype') == 'class'  # This should be 'class' for int
    
    # Verify that they have different reftypes (this confirms the fix works)
    assert none_result[0].get('reftype') != int_result[0].get('reftype')