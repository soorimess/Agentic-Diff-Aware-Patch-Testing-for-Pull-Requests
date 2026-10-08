"""
Regression test for sphinx-doc/sphinx#9602

This test ensures that Literal annotation values are not treated as class references
when nitpick mode is enabled, which would cause false positive warnings.
"""
from sphinx.addnodes import pending_xref

from sphinx.domains.python import _parse_annotation


def test_literal_annotation_values_dont_create_class_references():
    """
    Test that Literal annotation values like True/False are not treated as class references.
    
    The bug was that Literal[True] would be parsed such that "True" 
    would be treated as a class reference, causing nitpick mode to fail.
    
    This test verifies that literal values in Literal types are handled properly
    so they don't get converted to references to non-existent classes.
    """
    
    class MockEnv:
        def __init__(self):
            self.ref_context = {}
            self.domaindata = {}
            self.config = MockConfig()
    
    class MockConfig:
        def __init__(self):
            self.python_use_unqualified_type_names = False
    
    env = MockEnv()
    
    # Test the specific problematic case from the bug report
    annotation = 'Literal[True]'
    
    # Parse the annotation - this should work without issues in nitpick mode
    result = _parse_annotation(annotation, env)
    
    # The key test: literal values should NOT be treated as class references
    # In the buggy version, we get pending_xref nodes for literal values like "True"
    # These would cause nitpick warnings because there's no class "True"
    
    # Check that we don't have problematic pending_xref nodes for literal values
    pending_xrefs = [node for node in result if isinstance(node, pending_xref)]
    
    # Check specifically for problematic literal values that would cause nitpick warnings
    for node in pending_xrefs:
        reftarget = node.get('reftarget', '')
        # Literal values like True, False, None, numbers, strings should not
        # be treated as class references in nitpick mode
        assert reftarget not in ('True', 'False', 'None'), \
            f"Literal value '{reftarget}' incorrectly treated as class reference in {annotation}"


def test_literal_annotation_various_types():
    """
    Test various literal annotation types to ensure they all work correctly
    and don't cause nitpick warnings.
    """
    
    class MockEnv:
        def __init__(self):
            self.ref_context = {}
            self.domaindata = {}
            self.config = MockConfig()
    
    class MockConfig:
        def __init__(self):
            self.python_use_unqualified_type_names = False
    
    env = MockEnv()
    
    # Test different literal values that could cause issues in nitpick mode
    test_cases = [
        'Literal[True]',
        'Literal[False]', 
        'Literal[1]',
        'Literal["hello"]',
        'Literal[None]'
    ]
    
    for annotation in test_cases:
        result = _parse_annotation(annotation, env)
        
        # The result should be a list of nodes
        assert isinstance(result, list)
        assert len(result) > 0
        
        # Check that we don't have problematic pending_xref nodes for literal values
        pending_xrefs = [node for node in result if isinstance(node, pending_xref)]
        
        # Check specifically for problematic literal values
        for node in pending_xrefs:
            reftarget = node.get('reftarget', '')
            # Literal values like True, False, None, numbers, strings should not
            # be treated as class references in nitpick mode
            assert reftarget not in ('True', 'False', 'None'), \
                f"Literal value '{reftarget}' incorrectly treated as class reference in {annotation}"