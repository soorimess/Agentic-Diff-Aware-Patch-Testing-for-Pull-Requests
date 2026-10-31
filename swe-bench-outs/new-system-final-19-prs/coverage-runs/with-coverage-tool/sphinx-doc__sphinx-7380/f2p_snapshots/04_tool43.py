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
    # This should return an ASTCommaExpr object, not fail
    assert str(ast) == '(a, b)'