"""
Regression test for sphinx-doc/sphinx#7454

This test ensures that None type hints are consistently handled 
regardless of whether autodoc_typehints is set to 'description' or 'signature'.
"""
import os
import tempfile
from unittest.mock import patch

from sphinx.domains.python import _parse_annotation


def test_parse_annotation_none_reftype():
    """Test that None type hints get reftype='obj' instead of reftype='class'."""
    # Test the _parse_annotation function directly
    result = _parse_annotation('None')
    
    # Before the fix, this would create a pending_xref with reftype='class'
    # After the fix, this should create a pending_xref with reftype='obj'
    
    # The result should be a list with one element
    assert len(result) == 1
    node = result[0]
    
    # Check that it's a pending_xref node
    from sphinx.addnodes import pending_xref
    assert isinstance(node, pending_xref)
    
    # Check the reftype - this is the key difference the fix addresses
    # Before fix: reftype='class' (incorrect for None)
    # After fix: reftype='obj' (correct for None)
    reftype = node.get('reftype', None)
    assert reftype == 'obj', f"Expected reftype='obj' for None, got reftype='{reftype}'"


def test_parse_annotation_none_vs_other_types():
    """Test that None is handled differently from other types."""
    none_result = _parse_annotation('None')
    int_result = _parse_annotation('int')
    
    # Both should be lists with one node
    assert len(none_result) == 1
    assert len(int_result) == 1
    
    none_node = none_result[0]
    int_node = int_result[0]
    
    # Check that they have different reftypes (this is what the fix enables)
    none_reftype = none_node.get('reftype', None)
    int_reftype = int_node.get('reftype', None)
    
    # The fix ensures that None gets reftype='obj' while others get reftype='class'
    # This is the core behavior that was inconsistent
    assert none_reftype == 'obj'
    assert int_reftype == 'class'


def test_parse_annotation_consistency():
    """Test that the fix makes None handling consistent."""
    # Test multiple None cases to make sure they're all handled correctly
    test_cases = ['None', 'NoneType']  # NoneType is also a special case
    
    for case in test_cases:
        result = _parse_annotation(case)
        assert len(result) == 1
        node = result[0]
        from sphinx.addnodes import pending_xref
        assert isinstance(node, pending_xref)
        
        # For None specifically, it should get obj reftype
        if case == 'None':
            assert node.get('reftype') == 'obj'
        else:
            # Other cases should still get class reftype
            assert node.get('reftype') == 'class'