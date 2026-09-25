"""
Test for issue with C++ User Defined Literals (UDLs)

This test verifies that C++ user-defined literals like `6.62607015e-34q_J` 
and `1q_s` parse correctly rather than causing an "Expected end of definition" error.
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_user_defined_literals_not_causing_end_of_definition_error():
    """Test that user-defined literals are parsed rather than causing 'Expected end of definition' error"""
    
    # Test case from the bug report
    definition = "constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s;"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # Should NOT raise DefinitionError with "Expected end of definition"
    # This would indicate that UDL parsing is working correctly
    try:
        ast = parser.parse_declaration('member', 'member')
        # After parsing, all text should have been consumed
        # The assert_end() method is what would fail with our exact bug
        parser.assert_end()
        # If we get here, all was parsed successfully
        assert True  # Test passes if no exception thrown for the UDL case 
    except DefinitionError as e:
        # The specific bug we're trying to catch is this error message
        if "Expected end of definition" in str(e):
            pytest.fail(f"UDL parsing broken: {str(e)} - UDLs should be handled properly")
        raise


def test_float_literal_with_udl_parsing():
    """Test that float literal with UDL is fully parsed"""
    definition = "auto x = 3.14159q_pi;"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        # Verify that the full expression is consumed 
        parser.assert_end()
        assert True
    except DefinitionError as e:
        if "Expected end of definition" in str(e):
            pytest.fail(f"UDL parsing broken: {str(e)}")
        raise


def test_integer_literal_with_udl_parsing():
    """Test that integer literal with UDL is fully parsed"""  
    definition = "auto x = 42q_meter;"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        assert True
    except DefinitionError as e:
        if "Expected end of definition" in str(e):
            pytest.fail(f"UDL parsing broken: {str(e)}")
        raise


def test_string_literal_with_udl_parsing():
    """Test that string literal with UDL is fully parsed"""
    definition = 'auto x = "hello"q_str;'
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        assert True
    except DefinitionError as e:
        if "Expected end of definition" in str(e):
            pytest.fail(f"UDL parsing broken: {str(e)}")
        raise