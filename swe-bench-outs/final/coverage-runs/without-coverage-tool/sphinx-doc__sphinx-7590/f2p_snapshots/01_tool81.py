"""
Test for C++ User Defined Literals support.

This test verifies that C++ user defined literals (UDLs) are properly parsed
by Sphinx's C++ domain. The test specifically checks that UDLs don't leave 
unprocessed text, which was causing "Expected end of definition" errors.
"""

from sphinx.domains.cpp import DefinitionParser


def test_cpp_udl_no_unprocessed_text():
    """
    Test that UDL parsing consumes the entire definition without leaving text unprocessed.
    
    Before the fix: parsing "6.62607015e-34q_J" would consume only "6.62607015e-34" (14 chars)
    leaving "q_J" (3 chars) unprocessed, which would cause "Expected end of definition" error
    
    After the fix: parsing should consume all 17 characters successfully
    """
    
    definition = "6.62607015e-34q_J"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # Parse the literal
    result = parser._parse_literal()
    
    # The key assertion: the parser should consume the entire definition
    # If it doesn't, it means UDL parsing isn't working properly
    assert result is not None
    assert parser.pos == len(definition), f"Parser only consumed {parser.pos} of {len(definition)} characters"
    
    # The result should be a valid AST node (not None)
    # This test will fail before the fix because parser.pos will be 14 instead of 17


def test_cpp_udl_integer_with_suffix():
    """
    Test integer literal with UDL suffix.
    """
    definition = "42ul"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    result = parser._parse_literal()
    
    # Should consume entire definition
    assert result is not None
    assert parser.pos == len(definition), f"Parser only consumed {parser.pos} of {len(definition)} characters"


def test_cpp_udl_string_with_suffix():
    """
    Test string literal with UDL suffix.
    """
    definition = '"hello"sv'
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    result = parser._parse_literal()
    
    # Should consume entire definition
    assert result is not None
    assert parser.pos == len(definition), f"Parser only consumed {parser.pos} of {len(definition)} characters"


if __name__ == "__main__":
    test_cpp_udl_no_unprocessed_text()
    test_cpp_udl_integer_with_suffix()
    test_cpp_udl_string_with_suffix()
    print("All tests passed!")