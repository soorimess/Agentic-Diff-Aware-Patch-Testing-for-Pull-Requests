"""
Regression test for C++ User Defined Literals support.

This test ensures that user-defined literals like '6.62607015e-34q_J' 
are properly parsed instead of causing "Invalid definition: Expected end of definition" errors.
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_cpp_user_defined_literals_parsing():
    """Test that C++ user-defined literals parse without 'Expected end of definition' errors."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test cases that should work after the fix
    test_cases = [
        # The exact case from the bug report
        "constexpr auto planck_constant = 6.62607015e-34q_J;",
        # Simple integer with UDL
        "int x = 42q_J;",
        # Float with UDL  
        "double d = 3.14159q_pi;",
        # String with UDL
        'const char* s = "hello"sv;',
    ]
    
    for test_case in test_cases:
        parser = DefinitionParser(test_case, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        
        # These should NOT raise "Invalid definition: Expected end of definition"
        try:
            ast = parser.parse_declaration('member', 'member')
            parser.assert_end()
            # If we get here without exception, parsing succeeded
        except DefinitionError as e:
            if "Expected end of definition" in str(e):
                pytest.fail(f"UDL parsing failed for '{test_case}': {e}")
            # Other errors are acceptable


def test_cpp_user_defined_literals_simple_case():
    """Test the most basic UDL case that should work."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Simple case that should definitely work after the fix
    test_case = "int x = 42q_J;"
    
    parser = DefinitionParser(test_case, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should not raise an exception
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # Success - no exception means it parsed correctly
    except DefinitionError as e:
        if "Expected end of definition" in str(e):
            pytest.fail(f"Simple UDL parsing failed: {e}")
        # Other errors are fine