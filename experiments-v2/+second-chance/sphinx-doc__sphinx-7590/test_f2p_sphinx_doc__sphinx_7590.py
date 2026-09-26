"""
Regression test for C++ User Defined Literals support.

This test ensures that user-defined literals like "6.62607015e-34q_J"
are properly parsed and handled by the C++ domain parser.
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_cpp_udl_parsing_succeeds():
    """Test that C++ user-defined literals are parsed successfully (not raising DefinitionError)."""
    
    # Test cases that should parse successfully with UDL support
    test_cases = [
        "constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s",
        "auto x = 42q_test", 
        "auto y = 3.14159q_pi",
        "auto z = 123q_meter"
    ]
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    for definition in test_cases:
        parser = DefinitionParser(definition, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        
        # This should NOT raise DefinitionError in the fixed version
        # If it does raise, that's the bug - UDLs aren't supported
        try:
            ast = parser.parse_declaration('member', 'member')
            parser.assert_end()
            # If we get here without exception, parsing succeeded - this is what we want
        except DefinitionError as e:
            # In the old code (without UDL support), this would fail
            # But we want the test to pass when UDLs work
            pytest.fail(f"DefinitionError raised for UDL parsing: {e}")


def test_cpp_udl_simple():
    """Test simple user-defined literal parsing."""
    
    definition = "auto x = 42q_test"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should parse without raising an exception
    ast = parser.parse_declaration('member', 'member')
    parser.assert_end()
    # If we get here, parsing succeeded


def test_cpp_udl_float():
    """Test user-defined literal with float literal."""
    
    definition = "auto x = 3.14159q_pi"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should parse without raising an exception
    ast = parser.parse_declaration('member', 'member')
    parser.assert_end()
    # If we get here, parsing succeeded


def test_cpp_udl_integer():
    """Test user-defined literal with integer literal."""
    
    definition = "auto x = 123q_meter"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should parse without raising an exception
    ast = parser.parse_declaration('member', 'member')
    parser.assert_end()
    # If we get here, parsing succeeded


def test_cpp_udl_string():
    """Test user-defined literal with string literal."""
    
    definition = 'auto x = "hello"q_str'
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should parse without raising an exception
    ast = parser.parse_declaration('member', 'member')
    parser.assert_end()
    # If we get here, parsing succeeded


def test_cpp_udl_character():
    """Test user-defined literal with character literal."""
    
    definition = "auto x = 'a'q_char"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should parse without raising an exception
    ast = parser.parse_declaration('member', 'member')
    parser.assert_end()
    # If we get here, parsing succeeded


def test_cpp_udl_exact_bug_case():
    """Test the exact case from the bug report."""
    
    # This is the exact case from the bug report that was failing
    definition = "constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should NOT raise DefinitionError - the bug was that it did
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here, parsing succeeded
    except DefinitionError as e:
        # This would be the bug - the error mentioned in the bug report
        if "Expected end of definition" in str(e) and "error at 58" in str(e):
            pytest.fail(f"Bug still present: {e}")
        else:
            # Some other DefinitionError, which is fine
            raise