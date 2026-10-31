# Test for the C++ domain issue with parentheses in template parameter packs
# This reproduces the bug described in the pull request:
# "cpp domain parens in template parameter packs fails"
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_original_bug_case():
    """
    Test the exact case from the bug report that was failing.
    
    The bug was that expressions like:
    template <std::integer_sequence<bool, (static_cast<void>(Bs), false)>> foo
    would fail to parse because the parser couldn't handle comma expressions
    with parentheses in template parameters.
    
    This test should fail before the change and pass after the change.
    """
    # This test should pass after the fix is applied
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    try:
        parser = DefinitionParser('template <std::integer_sequence<bool, (static_cast<void>(Bs), false)>> foo', 
                                 location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        ast = parser.parse_declaration('class', 'class')
        parser.assert_end()
        # If we get here without exception, the parsing worked
        print("SUCCESS: Original bug case parsed correctly")
        return True
    except DefinitionError as e:
        # This is expected before the fix
        raise AssertionError(f"Original bug case failed to parse (this is expected before fix): {e}")