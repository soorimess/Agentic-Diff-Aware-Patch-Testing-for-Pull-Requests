"""
Regression test for inconsistent handling of None by autodoc_typehints.

This test directly tests the _parse_annotation function to verify that
None type hints are handled consistently regardless of autodoc_typehints mode.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from sphinx.domains.python import _parse_annotation
from sphinx.addnodes import pending_xref


def test_parse_annotation_none_handling():
    """Test that None annotation is handled correctly."""
    
    # Test the _parse_annotation function directly
    # This tests the core issue: None should be treated as 'obj' not 'class'
    
    # Parse a None annotation
    result = _parse_annotation('None')
    
    # The result should be a list with a pending_xref node
    assert len(result) == 1
    node = result[0]
    
    # Check that the node is a pending_xref with correct properties
    assert isinstance(node, pending_xref)
    
    # The reftype should be 'obj' for None, not 'class'
    # This is the fix that was applied - before it was always 'class'
    # Before the fix, this would fail because it returns 'class'
    # After the fix, it should return 'obj'
    assert node.get('reftype') == 'obj', f"Expected reftype 'obj' for None, got '{node.get('reftype')}'"
    
    # The reftarget should be 'None'
    assert node.get('reftarget') == 'None'
    
    # Test with other types to make sure we didn't break anything
    int_result = _parse_annotation('int')
    assert len(int_result) == 1
    int_node = int_result[0]
    assert isinstance(int_node, pending_xref)
    # For non-None types, it should still be 'class' 
    assert int_node.get('reftype') == 'class', f"Expected reftype 'class' for int, got '{int_node.get('reftype')}'"


def test_parse_annotation_consistency():
    """Test that the behavior is consistent for different inputs."""
    
    # Test various type annotations to make sure they work as expected
    test_cases = [
        ('None', 'obj'),  # Should be 'obj' for None
        ('int', 'class'),  # Should be 'class' for int
        ('str', 'class'),  # Should be 'class' for str
        ('list', 'class'),  # Should be 'class' for list
    ]
    
    for annotation, expected_reftype in test_cases:
        result = _parse_annotation(annotation)
        assert len(result) == 1
        node = result[0]
        assert isinstance(node, pending_xref)
        assert node.get('reftype') == expected_reftype, f"Expected reftype '{expected_reftype}' for '{annotation}', got '{node.get('reftype')}'"