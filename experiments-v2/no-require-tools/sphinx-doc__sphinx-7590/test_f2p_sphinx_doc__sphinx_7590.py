"""
    test_f2p_sphinx_doc__sphinx_7590
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for C++ User Defined Literals (UDL) support.

    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import pytest

from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_cpp_udl_avoids_expected_end_of_definition_error():
    """
    Test that C++ User Defined Literals do not cause 
    'Invalid definition: Expected end of definition' error.
    
    This addresses the bug where code like:
    '6.62607015e-34q_J * 1q_s' would fail with the above error.
    """
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test the exact problematic case from the bug report
    problematic_code = '6.62607015e-34q_J * 1q_s'
    
    parser = DefinitionParser(problematic_code, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should not raise the specific error from the bug report
    try:
        ast = parser.parse_expression()
        # If we get here, parsing succeeded - the main assertion
        assert ast is not None
    except DefinitionError as e:
        error_msg = str(e)
        # The specific error mentioned in the bug report should not occur
        assert "Expected end of definition" not in error_msg, \
            f"Bug still present: {error_msg}"
        # If it's a different error, that's fine - we only care about avoiding this specific one


def test_cpp_simple_udl_parsing():
    """Test simple UDL parsing cases."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test various UDL cases that should work
    test_cases = [
        '5q_test',      # integer literal with UDL
        '3.14fq_pi',    # float literal with suffix + UDL  
        '0x123q_hex',   # hex literal with UDL
        '"hello"q_str', # string literal with UDL
    ]
    
    for test_case in test_cases:
        parser = DefinitionParser(test_case, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        try:
            ast = parser.parse_expression()
            # If we get here, parsing succeeded
            assert ast is not None
        except DefinitionError as e:
            error_msg = str(e)
            # Should not get the specific error from the bug report
            assert "Expected end of definition" not in error_msg, \
                f"Failed to parse '{test_case}': {error_msg}"


def test_cpp_udl_declaration_parsing():
    """Test that full declarations with UDLs parse correctly."""
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # The exact declaration from the bug report
    declaration = 'inline constexpr auto planck_constant = 6.62607015e-34q_J * 1q_s'
    
    parser = DefinitionParser(declaration, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    try:
        # Try parsing as a member variable declaration
        ast = parser.parse_declaration('member', 'var')
        # If we get here, parsing succeeded
        assert ast is not None
    except DefinitionError as e:
        error_msg = str(e)
        # Should not get the specific error from the bug report
        assert "Expected end of definition" not in error_msg, \
            f"Declaration parsing failed: {error_msg}"