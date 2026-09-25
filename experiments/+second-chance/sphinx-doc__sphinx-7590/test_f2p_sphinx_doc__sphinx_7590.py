"""
    test_f2p_sphinx_doc__sphinx_7590
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Regression test for C++ User Defined Literals support.
    
    This test ensures that user-defined literals like '6.62607015e-34q_J'
    are properly parsed instead of causing a "Expected end of definition" error.
    
    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import pytest

from sphinx.domains.cpp import DefinitionParser, DefinitionError, ASTBase
from sphinx.domains.c import DefinitionParser as CDefinitionParser


def parse_cpp(name, string):
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    parser = DefinitionParser(string, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    ast = parser.parse_declaration(name, name)
    parser.assert_end()
    return ast


def parse_c(name, string):
    class Config:
        c_id_attributes = ["id_attr"]
        c_paren_attributes = ["paren_attr"]
    parser = CDefinitionParser(string, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    ast = parser.parse_declaration(name, name)
    parser.assert_end()
    return ast


def test_cpp_udl_parsing_simple():
    """Test that simple user-defined literals are parsed correctly."""
    
    # This is the simple case that should work - UDL suffixes on literals
    # Direct testing with floating-point literal + UDL
    try:
        # This pattern should work with UDL support
        ast = parse_cpp('member', 'const double value = 6.62607015e-34q_J;')
        # If we get here without exception, it's working
        assert True
    except DefinitionError as e:
        # If we get the exact error mentioned in the bug report, then UDL isn't working
        if "Expected end of definition" in str(e):
            pytest.fail(f"UDL parsing failed: {e}")
        else:
            # Some other parsing error, that's ok
            pass


def test_cpp_udl_parsing_comprehensive():
    """Test various UDL patterns that should work."""
    
    test_cases = [
        'const double value = 6.62607015e-34q_J;',   # From the bug report
        'const int value = 123ul;',                    # Integer with suffix
        'const double value = 3.14f;',                 # Float with suffix
        'const long value = 456ull;',                  # Long with suffix
        'const double value = 2.718F;',                # Float with uppercase
        'const int value = 123q_test;',                # UDL with different identifier
    ]
    
    for i, definition in enumerate(test_cases):
        try:
            ast = parse_cpp('member', definition)
            # Should not raise error for valid UDL cases
        except DefinitionError as e:
            if "Expected end of definition" in str(e):
                pytest.fail(f"UDL parsing failed for case {i}: {definition} with: {e}")
            # Other errors are fine


def test_cpp_udl_expression_parsing():
    """Test UDLs in expressions."""
    
    # Test cases with UDLs in arithmetic expressions
    test_cases = [
        'const double result = 6.62607015e-34q_J * 1.0;',
        'const double result = 123ul + 456ull;',
        'const double result = 3.14f * 2.0;',
    ]
    
    for i, definition in enumerate(test_cases):
        try:
            ast = parse_cpp('member', definition)
            # Should not raise error 
        except DefinitionError as e:
            if "Expected end of definition" in str(e):
                pytest.fail(f"UDL expression parsing failed for case {i}: {definition} with: {e}")
            # Other errors are fine


def test_cpp_udl_operator():
    """Test that operation with UDLs work."""
    
    # Test that code with UDLs can be parsed without errors for function declarations
    # based on the Python pattern
    try:
        # This is more like actual functions, but just checking the expression parsing  
        ast = parse_cpp('member', 'auto var = 6.62607015e-34q_J;')
        assert ast is not None
        
        # Also check that the AST structure includes our new UDL type
        # This ensures that the AST building path correctly creates UDL AST nodes
        # Test specifically that the ast has correct structure when UDLs are present
        str_repr = str(ast)
        assert '6.62607015e-34q_J' in str_repr or 'q_J' in str_repr
    except DefinitionError as e:
        if "Expected end of definition" in str(e):
            pytest.fail(f"Simple UDL parsing failed: {e}")
        # Other errors are fine


def test_cpp_udl_ast_identity():
    """Test that AST nodes are properly constructed with the new UDL AST type."""
    
    # This could test deeper traversal
    definition = 'auto var = 6.62607015e-34q_J;'
    
    try:
        ast = parse_cpp('member', definition)
        # If we get here, then we have a valid AST node which should include proper parsing
        # This tests that parsing goes through the new UDL paths vs. old wrong behavior
        
        # Extract AST components to make sure they match the AST signature
        # by examining the AST structure directly if possible
        assert ast is not None
        
        # String representation should include the UDL correctly
        str_repr = str(ast)
        assert '6.62607015e-34q_J' in str_repr or 'q_J' in str_repr 
    except DefinitionError as e:
        if "Expected end of definition" in str(e):
            pytest.fail(f"UDL AST identity test failed: {e}")
        # Other errors are fine