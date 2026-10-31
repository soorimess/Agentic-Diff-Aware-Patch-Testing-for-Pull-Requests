"""
Regression test for C++ User Defined Literals support.

This test verifies that C++ user-defined literals like:
    constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s;
are properly parsed and handled by Sphinx's C++ domain.
"""

from sphinx.domains.cpp import DefinitionParser, DefinitionError
from sphinx.util.cfamily import verify_description_mode


def test_udl_complex_expression_parsing():
    """Test that complex expressions with UDLs parse without 'Expected end of definition' error.
    
    This is the main issue reported: the specific case that caused:
    WARNING: Invalid definition: Expected end of definition. [error at 58]
    """
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # The exact case from the issue report that should now work
    test_case = "constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s"
    
    # Parse the complex expression - this should NOT raise "Expected end of definition"
    parser = DefinitionParser(test_case, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    result = parser.parse_declaration('member', 'var')
    parser.assert_end()
    
    # If we get here without an exception, the fix works
    # This is the main assertion - no "Expected end of definition" error
    assert result is not None, "Should successfully parse the complex UDL expression"


def test_udl_description_modes():
    """Test that UDL description modes work correctly."""
    
    # Test that the new 'udl' description mode is valid
    # This should not raise an exception - the assertion is that it doesn't raise
    verify_description_mode('udl')
    
    # If we get here, the function succeeded - this is our assertion
    assert True, "verify_description_mode should accept 'udl' mode without error"


def test_simple_udl_parsing():
    """Test simple UDL parsing works correctly."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test that we can parse a simple UDL without "Expected end of definition" error
    test_case = "42q_J"
    parser = DefinitionParser(test_case, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # Try to parse as expression - this should work for valid UDLs
    result = parser.parse_expression()
    
    # If we get here without an exception, the fix works
    # This is our assertion - the expression parsed successfully
    assert result is not None, "Should successfully parse simple UDL expression"


if __name__ == "__main__":
    print("Testing UDL parsing behavior...")
    test_udl_complex_expression_parsing()
    test_udl_description_modes()
    test_simple_udl_parsing()
    print("All tests completed successfully.")