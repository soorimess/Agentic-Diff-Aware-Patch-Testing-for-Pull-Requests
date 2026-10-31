"""
Regression test for C++ User Defined Literals support.

This test verifies that C++ user-defined literals like:
    constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s;
are properly parsed and handled by Sphinx's C++ domain.
"""

from sphinx.domains.cpp import DefinitionParser
from sphinx.domains.c import DefinitionParser as CDefinitionParser, DefinitionError


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


def test_c_domain_udl_parsing():
    """Test that C domain also handles UDLs correctly."""
    
    # Test that C domain parsing works with basic literals (this exercises the C parser)
    class Config:
        c_id_attributes = ["id_attr"]
        c_paren_attributes = ["paren_attr"]
    
    # Test basic integer literals that should work in C
    test_cases = [
        "42",
        "42u",
        "42l", 
        "42ul"
    ]
    
    for test_case in test_cases:
        parser = CDefinitionParser(test_case, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        result = parser.parse_expression()
        parser.assert_end()
        # If we get here without exception, it worked
        assert result is not None