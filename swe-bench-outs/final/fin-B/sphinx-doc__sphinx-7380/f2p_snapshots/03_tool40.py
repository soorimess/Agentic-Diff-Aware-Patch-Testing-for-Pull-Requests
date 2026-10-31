# Test for the specific issue with parentheses in template parameter packs
# This test verifies that comma expressions in parentheses can be parsed correctly

def test_comma_expressions_directly():
    """Test that comma expressions can be parsed directly.
    
    This tests the core functionality that was added in the fix - 
    parsing comma expressions like (a, b) correctly.
    """
    # Test parsing a comma expression directly - this should work after the fix
    from sphinx.domains.cpp import DefinitionParser
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    parser = DefinitionParser('(a, b)', location=None,
                              config=Config())
    parser.allowFallbackExpressionParsing = False
    ast = parser.parse_expression()
    res = str(ast)
    # This should work for comma expressions
    assert res == '(a, b)', f"Expected '(a, b)', got '{res}'"


def test_simple_template_declaration():
    """Test simple template syntax still works.
    
    This ensures we don't break existing functionality.
    """
    from sphinx.domains.cpp import DefinitionParser
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    parser = DefinitionParser('template<int> A', location=None,
                              config=Config())
    parser.allowFallbackExpressionParsing = False
    ast = parser.parse_declaration('class', 'class')
    # Should parse without error
    assert ast is not None