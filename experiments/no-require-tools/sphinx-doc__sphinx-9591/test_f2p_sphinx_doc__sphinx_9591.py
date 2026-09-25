"""
Regression test for "Cross-references don't work in property's type annotations" bug.

The fix addresses: when type annotations are processed, they should be parsed for 
cross-reference purposes, not treated as raw string content. 

This test validates that the change in behavior from:
OLD: signode += addnodes.desc_annotation(typ, ': ' + typ)  
NEW: annotations = _parse_annotation(typ, self.env); signode += addnodes.desc_annotation(typ, '', nodes.Text(': '), *annotations)

is present by checking source code structure.
"""

import inspect


def test_fix_in_pyattribute_source():
    """
    Validates that the Python domain's PyAttribute handle_signature method
    uses the correct pattern after the fix is applied.
    
    This specific test inspects the exact source code change to ensure 
    the proper annotation handling is in place.
    """
    # Import the class to examine source
    from sphinx.domains.python import PyAttribute
    
    # Get source lines for inspection
    source_lines = inspect.getsource(PyAttribute.handle_signature).split('\n')
    
    # Look for specific indicators that the fix has been applied:
    # 1. _parse_annotation should be called
    # 2. *annotations should be used in the desc_annotation call
    parse_annotation_found = False
    annotations_usage_found = False
    
    for line in source_lines:
        if 'parse_annotation' in line and 'annotations = ' in line:
            parse_annotation_found = True
        if '*annotations' in line and 'desc_annotation' in line:
            annotations_usage_found = True
    
    # These both must be true for the bug fix to be present
    assert parse_annotation_found, "Expected _parse_annotation call not found in PyAttribute.handle_signature"
    assert annotations_usage_found, "Expected *annotations usage not found in desc_annotation call"
    
    # Basic validation that we have made the right change-checking test
    assert True  # Defensive assertion to make sure test does not fail for no reason


def test_method_signature_contains_fix_indicators():
    """
    Most precise validation - we check the actual method lines to validate fix presence
    """
    from sphinx.domains.python import PyAttribute
    
    source = inspect.getsource(PyAttribute.handle_signature)
    
    # The method should have:
    # 1. annotations = _parse_annotation(typ, self.env)  
    # 2. signode += addnodes.desc_annotation(typ, '', nodes.Text(': '), *annotations)
    
    has_annotation_parse = 'annotations = _parse_annotation' in source
    has_proper_annotation_structure = '*annotations' in source and 'desc_annotation' in source
    
    # Both conditions should be met for the fix
    assert has_annotation_parse
    assert has_proper_annotation_structure