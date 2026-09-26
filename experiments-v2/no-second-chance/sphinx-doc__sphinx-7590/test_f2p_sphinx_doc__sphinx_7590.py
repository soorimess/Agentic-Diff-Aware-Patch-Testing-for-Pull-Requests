"""
Regression test for C++ User Defined Literals support.

This test ensures that UDLs like "6.62607015e-34q_J" are properly parsed
instead of causing "Invalid definition: Expected end of definition" errors.
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_cpp_udl_parsing_basic():
    """Test that basic C++ user-defined literals are parsed correctly."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test the exact case from the bug report
    test_case = "constexpr auto planck_constant = 6.62607015e-34q_J * 1q_s"
    parser = DefinitionParser(test_case, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    ast = parser.parse_declaration('member', 'member')
    parser.assert_end()
    assert ast is not None


def test_cpp_udl_various_formats():
    """Test UDLs with various literal formats and suffixes."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test various combinations that should work after the fix
    test_cases = [
        "constexpr auto value = 42ul_test",
        "constexpr auto value = 3.14f_pi", 
        "constexpr auto value = 0xFFul_test",
        "constexpr auto value = 123.456f_test",
        "constexpr auto value = 789.0l_test",
        "constexpr auto value = 0x1234ul_test",
        "constexpr auto value = 0b1010ul_test",
    ]
    
    for test_case in test_cases:
        parser = DefinitionParser(test_case, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        assert ast is not None


def test_cpp_udl_string_char():
    """Test UDLs with string and character literals."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test string and character literals with UDLs
    test_cases = [
        "constexpr auto value = \"hello\"_str",
        "constexpr auto value = 'c'_char",
    ]
    
    for test_case in test_cases:
        parser = DefinitionParser(test_case, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        assert ast is not None


if __name__ == "__main__":
    test_cpp_udl_parsing_basic()
    test_cpp_udl_various_formats()
    test_cpp_udl_string_char()
    print("All tests passed!")