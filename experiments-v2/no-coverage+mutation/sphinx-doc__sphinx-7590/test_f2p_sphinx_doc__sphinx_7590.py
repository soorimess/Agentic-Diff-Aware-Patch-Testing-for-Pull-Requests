"""
Regression test for C++ User Defined Literals support.

This test ensures that C++ User Defined Literals like `6.62607015e-34q_J` 
are properly parsed instead of causing "Invalid definition" errors.
"""
import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_cpp_udl_complex_expression():
    """Test complex expression with UDL - this should fail before fix."""
    # Complex case from the bug report that should work after fix
    definition = "constexpr auto planck_constant = 6.62607015e-34q_J"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should work without raising an error after the fix
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here, the parsing succeeded
        assert True
    except DefinitionError as e:
        # This is the error we want to fix
        pytest.fail(f"DefinitionError raised: {e}")


def test_cpp_udl_with_operator():
    """Test UDL in expression with operators - this should fail before fix."""
    # Case that was failing in the original bug report
    definition = "constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should work without raising an error after the fix
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here, the parsing succeeded
        assert True
    except DefinitionError as e:
        # This is the error we want to fix
        pytest.fail(f"DefinitionError raised: {e}")


def test_cpp_udl_string_literal():
    """Test string literal with UDL - this should also work."""
    definition = 'auto s = "hello"q'
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should work without raising an error after the fix
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here, the parsing succeeded
        assert True
    except DefinitionError as e:
        # This is the error we want to fix
        pytest.fail(f"DefinitionError raised: {e}")


if __name__ == "__main__":
    test_cpp_udl_complex_expression()
    test_cpp_udl_with_operator()
    test_cpp_udl_string_literal()