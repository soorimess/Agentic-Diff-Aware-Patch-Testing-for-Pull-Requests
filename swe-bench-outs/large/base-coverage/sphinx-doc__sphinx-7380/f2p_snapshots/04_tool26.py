"""
Regression test for sphinx-doc/sphinx#7380
Tests that C++ template parameter packs with parentheses in template arguments work correctly.
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_template_parameter_with_parentheses_comma_expression():
    """
    Test the exact case from the bug report:
    template <std::integer_sequence<bool, (static_cast<void>(Bs), false)>> foo
    """
    
    # This is the exact failing case from the bug report
    test_case = "template <std::integer_sequence<bool, (static_cast<void>(Bs), false)>> foo"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # This should work after the fix but would fail before the fix
    parser = DefinitionParser(test_case, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # The parsing should not raise an exception
    try:
        ast = parser.parse_declaration("class", "class")
        parser.assert_end()
        print("SUCCESS: Parentheses in template parameters with comma expression parsed correctly")
        
        # Additional verification: check that we can get a meaningful string representation
        str_repr = str(ast)
        assert "integer_sequence" in str_repr
        assert "(static_cast<void>(Bs), false)" in str_repr
        assert "template" in str_repr.lower()
        
        # Verify the AST structure is correct by checking key components
        # The main point is that it parsed without throwing DefinitionError
        print("SUCCESS: String representation contains expected elements")
        
    except DefinitionError as e:
        print(f"FAILED: {test_case}")
        print(f"Error: {e}")
        raise


def test_template_parameter_with_c_style_cast():
    """
    Test the second case from the bug report:
    template <std::integer_sequence<bool, (void(Bs), false)>> foo
    """
    
    # This is the second failing case from the bug report
    test_case = "template <std::integer_sequence<bool, (void(Bs), false)>> foo"
    
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # This should work after the fix but would fail before the fix
    parser = DefinitionParser(test_case, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # The parsing should not raise an exception
    try:
        ast = parser.parse_declaration("class", "class")
        parser.assert_end()
        print("SUCCESS: C-style cast parentheses in template parameters parsed correctly")
        
        # Additional verification: check that we can get a meaningful string representation
        str_repr = str(ast)
        assert "integer_sequence" in str_repr
        assert "(void(Bs), false)" in str_repr
        assert "template" in str_repr.lower()
        
        # Verify the AST structure is correct by checking key components
        print("SUCCESS: String representation contains expected elements")
        
    except DefinitionError as e:
        print(f"FAILED: {test_case}")
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    test_template_parameter_with_parentheses_comma_expression()
    test_template_parameter_with_c_style_cast()
    print("All tests completed successfully!")