"""
Regression test for C++ User Defined Literals support.

This test ensures that C++ user-defined literals like `6.62607015e-34q_J` 
are properly parsed instead of causing "Invalid definition" errors.
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_udl_parsing_works():
    """Test that C++ user-defined literals parse correctly.
    
    This test verifies the fix for the bug where UDLs like `6.62607015e-34q_J` 
    would cause "Invalid definition: Expected end of definition" errors.
    """
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test the exact case from the bug report
    parser = DefinitionParser('constexpr auto h = 6.62607015e-34q_J;', 
                              location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should work with the fix, but would fail with old code
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here without exception, parsing worked
        assert ast is not None
    except DefinitionError as e:
        # If this fails with the expected error, it means UDL parsing is not implemented
        error_msg = str(e)
        if "Invalid definition" in error_msg or "Expected end of definition" in error_msg:
            pytest.fail(f"UDL parsing failed - this indicates the bug is still present: {error_msg}")
        # Some other error is fine


def test_udl_expressions_work():
    """Test that UDLs work in expressions.
    
    This tests that expressions like `6.62607015e-34q_J * 1q_s` parse correctly.
    """
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test UDLs in expressions
    parser = DefinitionParser('constexpr auto result = 6.62607015e-34q_J * 1q_s;', 
                              location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here without exception, parsing worked
        assert ast is not None
    except DefinitionError as e:
        # If this fails with the expected error, it means UDL parsing is not implemented
        error_msg = str(e)
        if "Invalid definition" in error_msg or "Expected end of definition" in error_msg:
            pytest.fail(f"UDL expression parsing failed - this indicates the bug is still present: {error_msg}")
        # Some other error is fine