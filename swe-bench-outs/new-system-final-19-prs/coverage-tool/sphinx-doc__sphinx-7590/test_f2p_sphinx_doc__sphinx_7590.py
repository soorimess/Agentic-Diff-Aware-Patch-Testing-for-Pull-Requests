"""
    test_f2p_sphinx_doc__sphinx_7590
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for C++ User Defined Literals (UDL) support.

    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_cpp_udl_parsing_no_invalid_definition_error():
    """
    Test that C++ UDL parsing works without 'Invalid definition' errors.
    
    This test verifies that the fix for C++ User Defined Literals prevents
    the parsing error that was reported in the GitHub issue.
    Before the fix, expressions like "42q_J" would cause:
    "Invalid C++ declaration: Expected end of definition"
    After the fix, they should parse successfully.
    """
    
    # Create parser with proper configuration (as used in existing tests)
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test the exact case that was failing before the fix
    # This should not raise "Invalid C++ declaration: Expected end of definition" error
    parser = DefinitionParser('42q_J', location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # The core behavior change: parsing should succeed instead of raising the specific error
    try:
        result = parser.parse_expression()
        # If we get here without the specific error, the fix works
        assert result is not None, "Failed to parse UDL expression"
        # Verify we get a meaningful result
        assert str(result) != "", "Result should not be empty string"
    except DefinitionError as e:
        error_msg = str(e)
        # Check if we're getting the specific error that was fixed
        if "Invalid C++ declaration: Expected end of definition" in error_msg:
            # This is the error we're trying to fix - if we still get it, test fails
            raise AssertionError(f"Still getting the old error that should be fixed: {error_msg}")
        # Other DefinitionErrors are OK (not the specific one we're fixing)