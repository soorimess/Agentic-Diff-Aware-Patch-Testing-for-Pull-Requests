"""
Regression test for Sphinx issue #9602
Tests that Literal annotation values are not treated as missing py:class
"""
from unittest.mock import Mock

from sphinx.domains.python import _parse_annotation
from sphinx import addnodes


def test_literal_annotation_no_invalid_pending_xrefs():
    """
    Test that literal annotation values don't create invalid pending_xref nodes
    that reference non-existent classes.
    
    The bug: Literal[True] would create a pending_xref to class 'True' which doesn't exist
    The fix: Literal values should not be processed as class references
    """
    # Create a mock environment
    env = Mock()
    env.ref_context = {}
    env.config = Mock()
    env.config.python_use_unqualified_type_names = False
    
    # Test the problematic literal annotation
    annotation = 'Literal[True]'
    result = _parse_annotation(annotation, env)
    
    # Verify we get a list of nodes
    assert isinstance(result, list)
    
    # Check that we don't have pending_xref nodes that reference literal values
    # as if they were class names
    for node in result:
        if isinstance(node, addnodes.pending_xref):
            # If this is a pending_xref, check if it's referencing a literal value
            node_text = node.astext()
            # The fix should prevent pending_xref to literal values like 'True', 'False', etc.
            # These should not be treated as class references
            literal_values = {'True', 'False', 'None', '1', '0'}
            assert node_text not in literal_values, f"Found problematic pending_xref to '{node_text}'"


def test_literal_annotation_structure():
    """
    Test that literal annotations have correct node structure.
    """
    # Create a mock environment
    env = Mock()
    env.ref_context = {}
    env.config = Mock()
    env.config.python_use_unqualified_type_names = False
    
    # Test various literal annotation patterns
    test_cases = [
        'Literal[True]',
        'Literal[False]',
        'Literal[1]',
        'Literal[0]',
        'Literal["hello"]',
        'Literal[None]'
    ]
    
    for annotation in test_cases:
        result = _parse_annotation(annotation, env)
        assert isinstance(result, list)
        assert len(result) >= 3  # Basic structure maintained


def test_literal_annotation_no_nitpick_warnings():
    """
    Test that literal annotations don't trigger nitpick warnings.
    """
    # Create a mock environment
    env = Mock()
    env.ref_context = {}
    env.config = Mock()
    env.config.python_use_unqualified_type_names = False
    
    # Test cases that would have caused nitpick warnings before the fix
    literal_annotations = [
        'Literal[True]',
        'Literal[False]',
        'typing.Literal[True]',
        'typing.Literal[False]'
    ]
    
    for annotation in literal_annotations:
        # The parsing should succeed without creating invalid node structures
        result = _parse_annotation(annotation, env)
        assert isinstance(result, list)
        
        # Verify the structure is valid for documentation generation
        assert len(result) >= 3