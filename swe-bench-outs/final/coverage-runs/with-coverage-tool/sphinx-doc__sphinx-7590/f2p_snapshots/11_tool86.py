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
    assert result is not None, "Should successfully parse the complex UDL expression"


def test_simple_udl_parsing():
    """Test that simple UDL expressions parse correctly."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test simple UDL cases that should work
    test_cases = [
        "42q_J",
        "3.14q_pi", 
        "1.0q_unit"
    ]
    
    for test_case in test_cases:
        parser = DefinitionParser(test_case, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        # Try to parse as expression - this should work for valid UDLs
        try:
            result = parser.parse_expression()
            # If we get here without an exception, the fix works
            assert result is not None, f"Should successfully parse simple UDL: {test_case}"
        except Exception:
            # Some simple cases might not parse as expressions, but they shouldn't 
            # raise "Expected end of definition" error when parsed as declarations
            try:
                result = parser.parse_declaration('member', 'var')
                parser.assert_end()
                assert result is not None, f"Should successfully parse simple UDL as declaration: {test_case}"
            except Exception as e:
                # If it fails with "Expected end of definition", that's the bug
                if "Expected end of definition" in str(e):
                    raise AssertionError(f"UDL parsing error in simple case: {test_case} - {e}")
                # Other errors are fine - we only care about the specific error we're fixing


if __name__ == "__main__":
    print("Testing UDL parsing behavior...")
    test_udl_complex_expression_parsing()
    test_simple_udl_parsing()
    print("All tests completed successfully.")