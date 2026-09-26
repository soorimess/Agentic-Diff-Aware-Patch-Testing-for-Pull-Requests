"""
Regression test for user-defined literals (UDL) support in C++ domain.

This test ensures that C++ code with user-defined literals like:
    constexpr auto planck_constant = 6.62607015e-34q_J * 1q_s;

is parsed correctly without errors.
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_user_defined_literals_basic():
    """Test that user-defined literals parse without errors."""
    # This is the exact case from the bug report that should work
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(
        "constexpr auto planck_constant = 6.62607015e-34q_J * 1q_s;", 
        location=None, config=Config()
    )
    parser.allowFallbackExpressionParsing = False
    
    # This should not raise a DefinitionError in the fixed version
    # The old version would fail with "Invalid definition: Expected end of definition"
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here without exception, the parsing succeeded
    except DefinitionError as e:
        # If this fails, it means the UDL parsing is not working
        # This would be the error in the broken version
        pytest.fail(f"User-defined literal parsing failed with error: {e}")


def test_user_defined_literals_simple():
    """Test simple user-defined literal parsing."""
    # Test a simple UDL like 42q_foo
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser("auto x = 42q_foo;", location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here, the parsing succeeded
    except DefinitionError as e:
        pytest.fail(f"Simple UDL parsing failed with error: {e}")


def test_user_defined_literals_float():
    """Test user-defined literal with float literal."""
    # Test a float UDL like 3.14159q_pi
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser("auto x = 3.14159q_pi;", location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here, the parsing succeeded
    except DefinitionError as e:
        pytest.fail(f"Float UDL parsing failed with error: {e}")


def test_user_defined_literals_string():
    """Test user-defined literal with string literal."""
    # Test a string UDL like "hello"q_str
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser('auto x = "hello"q_str;', location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here, the parsing succeeded
    except DefinitionError as e:
        pytest.fail(f"String UDL parsing failed with error: {e}")