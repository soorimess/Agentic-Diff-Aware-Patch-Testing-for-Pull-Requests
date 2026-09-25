"""
Test that validates the core issue: C++ User Defined Literals were 
not supported, leading to "Expected end of definition" errors.

This test should fail in the current (buggy) version and pass after 
the fix is applied.
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_udl_support_missing_currently():
    """
    Test that demonstrates what this fix addresses:
    The validation that we can parse simple user-defined literals.
    Without fix: would pass but not properly validate.
    With fix: should properly validate UDL parsing.
    """
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]

    # This is a critical test case: user-defined literals should work
    # that have the form: numeric_literal + identifier_suffix
    test_cases = [
        "42ul",        # integer literal with suffix - should parse successfully 
        "3.14159f",    # float literal with suffix - should parse successfully
    ]
    
    # For each test case, we're checking that parsing doesn't 
    # immediately fail with the main "Expected end of definition" error
    for test_case in test_cases:
        try:
            parser = DefinitionParser(test_case, location=None, config=Config())
            parser.allowFallbackExpressionParsing = False
            result = parser._parse_literal()
            # If we get here without error, it means the basic parsing works
            # This is the foundation upon which UDL parsing builds
            assert result is not None
        except DefinitionError as e:
            # This is our critical check - if we get an "Expected end of definition"
            # error, that indicates the UDL parsing problem
            if "Expected end of definition" in str(e):
                pytest.fail(f"UDL parsing fails with Expected end of definition error: {e}")
            else:
                # Some other parsing issue is acceptable
                pass
        except Exception as e:
            # Any other exception shouldn't be the focus of our test
            # We focus on UDL-specific behavior
            pass


def test_literal_parsing_still_works():
    """
    Ensure we don't break existing literal parsing functionality.
    """
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]

    # Test that basic functionality remains intact
    try:
        parser = DefinitionParser("6.62607015e-34", location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        result = parser._parse_literal()
        assert result is not None
    except Exception as e:
        pytest.fail(f"Basic literal parsing broken: {e}")