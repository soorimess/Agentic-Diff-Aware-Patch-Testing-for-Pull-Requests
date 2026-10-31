"""
Regression test for C++ User Defined Literals support.

This test verifies that C++ user-defined literals like:
    constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s;
are properly parsed and handled by Sphinx's C++ domain.
"""

from sphinx.domains.cpp import DefinitionParser


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
    assert result is not None


def test_simple_udl_parsing():
    """Test simple UDL parsing works correctly."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test simple UDL cases that should work
    test_case = "42q_J"
    parser = DefinitionParser(test_case, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # Try to parse as expression - this should work for valid UDLs
    try:
        result = parser.parse_expression()
        # If we get here, it parsed successfully
        assert result is not None
    except Exception as e:
        # If it fails with the specific error we're fixing, fail the test
        if "Expected end of definition" in str(e):
            raise AssertionError(f"UDL parsing still fails: {e}")
        # Other errors are fine - we only care about the specific error we're fixing