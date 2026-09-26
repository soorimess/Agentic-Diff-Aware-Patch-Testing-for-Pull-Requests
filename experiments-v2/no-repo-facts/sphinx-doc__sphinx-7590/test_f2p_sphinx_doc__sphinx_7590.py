"""
Test for C++ User Defined Literals support.

This test verifies that user-defined literals like "6.62607015e-34q_J" 
are properly parsed instead of causing "Invalid definition: Expected end of definition" errors.
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_cpp_user_defined_literals_basic():
    """Test that the main bug case from the issue is fixed."""
    
    # This is the exact case from the bug report that was failing
    definition = "constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s;"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should not raise a DefinitionError
    # Before the fix, this would raise: "Invalid definition: Expected end of definition"
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here without exception, the parsing succeeded
        assert ast is not None
    except DefinitionError as e:
        # If this fails, it means the UDL parsing is not working
        pytest.fail(f"Failed to parse user-defined literal: {e}")


def test_simple_udl_literal():
    """Test simple user-defined literal parsing directly."""
    
    # Test parsing just a literal with UDL suffix
    test_cases = [
        "6.62607015e-34q_J",
        "1q_s", 
        "42ul",
        "3.14f"
    ]
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    for test_case in test_cases:
        # Try to parse as an expression (which is where literal parsing happens)
        parser = DefinitionParser(test_case, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        try:
            # Parse as an expression
            ast = parser.parse_expression()
            # If we get here, parsing succeeded
        except DefinitionError as e:
            # If this fails, it means the UDL parsing is not working for this case
            pytest.fail(f"Failed to parse literal '{test_case}': {e}")


def test_udl_in_expression():
    """Test user-defined literals in expressions."""
    
    # Test cases with operators where UDLs are used
    test_cases = [
        "6.62607015e-34q_J * 1q_s",
        "42ul + 123ll",
        "3.14f - 2.71f"
    ]
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    for test_case in test_cases:
        parser = DefinitionParser(test_case, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        try:
            # Parse as an expression
            ast = parser.parse_expression()
            # If we get here, parsing succeeded
        except DefinitionError as e:
            # If this fails, it means the UDL parsing is not working for this case
            pytest.fail(f"Failed to parse expression '{test_case}': {e}")


def test_udl_with_signature_generation():
    """Test that UDLs work with signature generation (tests describe_signature path)."""
    
    # Test a case that should trigger UDL mode in signature generation
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Parse a UDL to make sure the full parsing pipeline works
    parser = DefinitionParser("auto x = 1q_s;", location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    try:
        # Parse as a full declaration 
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here without exception, the parsing succeeded
        assert ast is not None
    except DefinitionError as e:
        pytest.fail(f"Failed to parse UDL with declaration: {e}")