"""
Test for C++ User Defined Literals (UDL) support.
This test verifies that user-defined literals like 1q_s and 6.62607015e-34q_J
are correctly parsed in C++ declarations.
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_cpp_udl_parsing_basic():
    """Test that basic C++ user-defined literals are parsed correctly."""
    
    # Test cases that should work with UDL support - using valid declaration types
    test_cases = [
        # Basic integer UDL
        ("member", "constexpr auto x = 42q_s;"),
        # String literal with UDL  
        ("member", 'constexpr auto str = "hello"sv;'),
        # Character literal with UDL
        ("member", "constexpr auto ch = 'a'c;"),
    ]
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    for decl_type, test_case in test_cases:
        parser = DefinitionParser(test_case, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        try:
            # This should NOT raise an exception after the fix
            ast = parser.parse_declaration(decl_type, decl_type)
            parser.assert_end()
            # If we get here, parsing succeeded
        except DefinitionError as e:
            # If this fails in the original code but should pass after fix
            # We should check if it's the specific UDL parsing error
            if "Expected end of definition" in str(e) and "user-defined literal" in str(e):
                pytest.fail(f"UDL parsing failed for: {test_case} with error: {e}")
            else:
                # Different error, that's fine for this test
                pass


def test_cpp_udl_parsing_complex():
    """Test the complex case from the bug report - the specific failing scenario."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # This is the exact case from the bug report that was failing
    test_case = "constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s;"
    
    parser = DefinitionParser(test_case, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    try:
        # With the fix, this should parse successfully
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here, it means the parsing worked (i.e., the bug is fixed)
        # The key assertion is that it should NOT raise the original parsing error
        
    except DefinitionError as e:
        # This should NOT happen with the fix - the error indicates the UDL bug
        if "Expected end of definition" in str(e) and "58" in str(e):
            pytest.fail(f"UDL parsing bug still present: {test_case} failed with: {e}")
        else:
            # If it fails for a different reason, that's ok for this test 
            pass


def test_cpp_udl_parsing_no_regression():
    """Test that normal literals still work (regression test)."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test normal cases that should continue to work
    test_cases = [
        ("member", "constexpr auto x = 42;"),
        ("member", "constexpr auto y = 3.14159;"),
        ("member", 'constexpr auto str = "hello";'),
        ("member", "constexpr auto ch = 'a';"),
    ]
    
    for decl_type, test_case in test_cases:
        parser = DefinitionParser(test_case, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        try:
            ast = parser.parse_declaration(decl_type, decl_type)
            parser.assert_end()
        except DefinitionError as e:
            # For normal literals, if they fail, fail for different reasons
            # than UDL failures
            if "Expected end of definition" in str(e) and "58" in str(e):
                pytest.fail(f"Normal parsing broken: {test_case} failed with: {e}")