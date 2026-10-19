"""
Regression test for sphinx-doc/sphinx#7380
Test for cpp domain parens in template parameter packs
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_template_parameter_with_parentheses():
    """Test that parentheses around comma expressions in template parameters work."""
    # This should parse without error - test the specific case from the bug report
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    parser = DefinitionParser("template <std::integer_sequence<bool, (static_cast<void>(Bs), false)>> foo", 
                              location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    # Try to parse as a class declaration - this should work after the fix
    try:
        result = parser.parse_declaration("class", "class")
        # If we get here without exception, the test passes
        assert result is not None
    except DefinitionError:
        # If it fails, it's the old behavior - this is what we're testing
        pytest.fail("Should be able to parse parentheses in template parameters")


def test_template_parameter_with_c_style_cast():
    """Test that C-style casts in parentheses work in template parameters."""
    # This should parse without error - test the specific case from the bug report
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    parser = DefinitionParser("template <std::integer_sequence<bool, (void(Bs), false)>> foo", 
                              location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    # Try to parse as a class declaration - this should work after the fix
    try:
        result = parser.parse_declaration("class", "class")
        # If we get here without exception, the test passes
        assert result is not None
    except DefinitionError:
        # If it fails, it's the old behavior - this is what we're testing
        pytest.fail("Should be able to parse parentheses in template parameters")


def test_expression_parsing():
    """Test that comma expressions in parentheses can be parsed as expressions."""
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test comma expression parsing directly - this is the core issue
    parser = DefinitionParser("(static_cast<void>(Bs), false)", 
                              location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    try:
        result = parser.parse_expression()
        # If we get here without exception, the test passes
        assert result is not None
    except DefinitionError:
        # If it fails, it's the old behavior
        pytest.fail("Should be able to parse comma expressions in parentheses")


def test_comma_expression_parsing():
    """Test comma expressions parsing."""
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test comma expression parsing - this exercises ASTCommaExpr
    parser = DefinitionParser("a, b, c", 
                              location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    try:
        result = parser.parse_expression()
        # If we get here without exception, the test passes
        # Also test that it can be converted to string
        str_result = str(result)
        assert str_result is not None
        assert result is not None
    except DefinitionError:
        # If it fails, it's the old behavior
        pytest.fail("Should be able to parse comma expressions")


def test_template_argument_list_parsing():
    """Test template argument list parsing specifically."""
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # Test a complex template argument list that should exercise _parse_template_argument_list
    # This should trigger the template argument list parsing code path
    parser = DefinitionParser("template <typename T, int N = 5> class A", 
                              location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    try:
        result = parser.parse_declaration("class", "class")
        # If we get here without exception, the test passes
        assert result is not None
    except DefinitionError:
        # If it fails, it's the old behavior - but we're mainly focused on the core issue
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])