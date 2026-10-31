"""
Test for C++ User Defined Literals support.

This test verifies that C++ user defined literals (UDLs) are properly parsed
by Sphinx's C++ domain. The test ensures that UDLs don't leave unprocessed text,
which was causing "Expected end of definition" errors.
"""

from sphinx.domains.cpp import DefinitionParser


def test_cpp_udl_consumes_full_definition():
    """
    Test that UDL parsing consumes the entire definition without leaving text unprocessed.
    
    This test verifies that the fix for C++ User Defined Literals works correctly.
    Before the fix, parsing "6.62607015e-34q_J" would only consume 14 of 17 characters,
    leaving "q_J" unprocessed and causing "Expected end of definition" errors.
    After the fix, all characters should be consumed.
    """
    
    definition = "6.62607015e-34q_J"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # Parse the literal
    result = parser._parse_literal()
    
    # The fix ensures that the entire definition is consumed
    assert result is not None
    assert parser.pos == len(definition), f"Parser only consumed {parser.pos} of {len(definition)} characters"


def test_cpp_udl_string_with_suffix_consumes_full():
    """
    Test that string UDLs consume the entire definition.
    """
    
    definition = '"hello"sv'
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    parser = DefinitionParser(definition, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # Parse the literal
    result = parser._parse_literal()
    
    # The fix ensures that the entire definition is consumed
    assert result is not None
    assert parser.pos == len(definition), f"Parser only consumed {parser.pos} of {len(definition)} characters"


if __name__ == "__main__":
    test_cpp_udl_consumes_full_definition()
    test_cpp_udl_string_with_suffix_consumes_full()
    print("All tests passed!")