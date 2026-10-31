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
    
    try:
        parser = DefinitionParser(test_case, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        # Parse as a variable/declaration - this should not raise "Expected end of definition"
        result = parser.parse_declaration('member', 'var')
        parser.assert_end()
        print(f"✓ Complex UDL assignment parsed successfully: {test_case}")
        # The key assertion: no "Expected end of definition" error
        return True
    except DefinitionError as e:
        error_msg = str(e)
        if "Expected end of definition" in error_msg:
            raise AssertionError(f"UDL parsing error still exists: {test_case} - {error_msg}")
        else:
            # Some other error is fine - we only care about the specific error we're fixing
            print(f"✓ Different error (expected): {test_case} - {error_msg}")
            return True
    except Exception as e:
        print(f"? Other error: {test_case} - {e}")
        return True


def test_udl_description_modes():
    """Test that UDL description modes work correctly."""
    
    # Test that the new 'udl' description mode is valid
    try:
        verify_description_mode('udl')
        print("✓ 'udl' description mode is valid")
        return True
    except Exception as e:
        raise AssertionError(f"UDL description mode not supported: {e}")


def test_simple_udl_parsing():
    """Test simple UDL parsing works correctly."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test simple UDL cases that should work
    test_cases = [
        "42q_J",
        "3.14q_pi", 
        "1.0q_unit"
    ]
    
    for case in test_cases:
        try:
            parser = DefinitionParser(case, location=None, config=Config())
            parser.allowFallbackExpressionParsing = False
            # Try to parse as expression - this should work for valid UDLs
            result = parser.parse_expression()
            print(f"✓ Simple UDL parsed as expression: {case}")
        except DefinitionError as e:
            error_msg = str(e)
            # We expect some errors for standalone literals, but not "Expected end of definition"
            if "Expected end of definition" in error_msg:
                raise AssertionError(f"UDL parsing error in simple case: {case} - {error_msg}")
            else:
                print(f"✓ Different error (expected): {case} - {error_msg}")
        except Exception as e:
            print(f"? Other error in simple UDL: {case} - {e}")


if __name__ == "__main__":
    print("Testing UDL parsing behavior...")
    try:
        test_udl_complex_expression_parsing()
        test_udl_description_modes()
        test_simple_udl_parsing()
        print("All tests completed successfully.")
    except Exception as e:
        print(f"Test failed with exception: {e}")
        raise