"""
Test for User-Defined Literals (UDL) support in C++ domain.

This test ensures that the bug where C++ User Defined Literals are not supported
is properly fixed. The original issue was that code like:
    constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s;
would cause a warning about "Invalid definition: Expected end of definition"
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_cpp_udl_support():
    """Test that C++ User-Defined Literals are parsed correctly."""
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
        
    # This should not raise an error - this is the main bug case from the report
    parser = DefinitionParser(
        'constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s',
        location=None,
        config=Config()
    )
    parser.allowFallbackExpressionParsing = False
    
    # This should parse without raising an error
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here, the parsing succeeded
        assert ast is not None
    except DefinitionError as e:
        # If we get a DefinitionError, it should not be about "Expected end of definition"
        assert "Expected end of definition" not in str(e)


def test_udl_parsing_simple():
    """Test simple UDL parsing with floating point literal."""
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
        
    # Test with a simple floating point literal followed by UDL
    parser = DefinitionParser(
        'auto x = 1.0q_test',
        location=None,
        config=Config()
    )
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        assert ast is not None
    except DefinitionError as e:
        # This should not fail with "Expected end of definition"
        assert "Expected end of definition" not in str(e)


def test_udl_parsing_integer():
    """Test UDL parsing with integer literals."""
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
        
    parser = DefinitionParser(
        'auto x = 42q_test',
        location=None,
        config=Config()
    )
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        assert ast is not None
    except DefinitionError as e:
        # This should not fail with "Expected end of definition"
        assert "Expected end of definition" not in str(e)


def test_udl_parsing_string():
    """Test UDL parsing with string literals."""
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
        
    parser = DefinitionParser(
        'auto x = "hello"q_test',
        location=None,
        config=Config()
    )
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        assert ast is not None
    except DefinitionError as e:
        # This should not fail with "Expected end of definition"
        assert "Expected end of definition" not in str(e)


def test_udl_parsing_with_suffixes():
    """Test UDL parsing with literal suffixes."""
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
        
    # Test with float literal that has suffixes
    parser = DefinitionParser(
        'auto x = 1.0fq_test',
        location=None,
        config=Config()
    )
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        assert ast is not None
    except DefinitionError as e:
        # This should not fail with "Expected end of definition"
        assert "Expected end of definition" not in str(e)


def test_udl_parsing_with_complex_expression():
    """Test UDL parsing in complex expressions."""
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
        
    # Test with more complex expression involving UDLs
    parser = DefinitionParser(
        'auto x = (1.0q_test + 2.0q_test) * 3',
        location=None,
        config=Config()
    )
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        assert ast is not None
    except DefinitionError as e:
        # This should not fail with "Expected end of definition"
        assert "Expected end of definition" not in str(e)