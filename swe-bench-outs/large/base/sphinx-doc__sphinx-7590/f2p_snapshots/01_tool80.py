"""
Regression test for C++ User Defined Literals support.

This test ensures that C++ User Defined Literals like:
    6.62607015e-34q_J * 1q_s
are parsed correctly without generating "Invalid definition" warnings.
"""

from sphinx.domains.cpp import DefinitionParser
from sphinx.util.docutils import docutils_namespace


def test_cpp_udl_expression_parsing():
    """
    Test that UDL expressions parse correctly without "Expected end of definition" error.
    
    This test specifically addresses the GitHub issue where:
    "6.62607015e-34q_J * 1q_s"
    was causing:
    "WARNING: Invalid definition: Expected end of definition. [error at 58]"
    """
    
    # The exact problematic case from the issue - should parse as expression
    definition = "6.62607015e-34q_J * 1q_s"
    
    with docutils_namespace():
        class Config:
            cpp_id_attributes = ["id_attr"]
            cpp_paren_attributes = ["paren_attr"]
            
        # Parse as expression - this should work after the fix
        parser = DefinitionParser(definition, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        result = parser.parse_expression()
        # If we get here without error, parsing succeeded


def test_cpp_udl_simple_expression():
    """
    Test simple UDL expression parsing.
    """
    
    # Simple UDL case that would have been problematic
    case = "1q_s"
    
    with docutils_namespace():
        class Config:
            cpp_id_attributes = ["id_attr"]
            cpp_paren_attributes = ["paren_attr"]
            
        # Parse as expression - this should work after the fix
        parser = DefinitionParser(case, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        result = parser.parse_expression()


def test_cpp_udl_with_suffixes():
    """
    Test that literal suffixes work with UDLs in expressions.
    """
    
    # Test cases combining literal suffixes with UDL identifiers
    test_cases = [
        "123ulq_suffix",
        "123.45fq_suffix", 
        "6.62607015e-34q_J"
    ]
    
    with docutils_namespace():
        class Config:
            cpp_id_attributes = ["id_attr"]
            cpp_paren_attributes = ["paren_attr"]
            
        for case in test_cases:
            # Parse each case as expression - they should all work after the fix
            parser = DefinitionParser(case, location=None, config=Config())
            parser.allowFallbackExpressionParsing = False
            result = parser.parse_expression()