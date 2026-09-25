"""
Regression test for C++ User Defined Literals (UDL) support.
This test ensures that expressions like 6.62607015e-34q_J are parsed correctly
instead of causing "Invalid definition: Expected end of definition" errors.
"""

import pytest
from sphinx.domains.cpp import DefinitionParser, DefinitionError
from sphinx.util import docutils


def test_user_defined_literals_basic():
    """Test basic user defined literal parsing - should work after fix."""
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    # This is the basic test case that should work after UDL support is implemented
    input_text = "int x = 42q_test;"
    
    parser = DefinitionParser(input_text, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This should succeed with the fix
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here without exception, UDL support is working  
        assert ast is not None
    except DefinitionError as e:  
        # The specific error that signifies the old buggy behavior
        if "Expected end of definition" in str(e):
            pytest.fail("UDL support not implemented: parsing fails with 'Expected end of definition' error")
        else:
            # Some other parsing error - that's okay
            raise e


def test_user_defined_literals_with_float():
    """Test UDL with float literal - exact case from bug report."""
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
        
    # This is the exact case from the bug report that should work after fix
    input_text = "constexpr auto planck_constant = 6.62607015e-34q_J * 1q_s;"
    
    parser = DefinitionParser(input_text, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    try:
        ast = parser.parse_declaration('member', 'member')
        parser.assert_end()
        # If we get here, the parsing succeeded 
        assert ast is not None
    except DefinitionError as e:
        # If this fails with expected error, it means the fix isn't applied
        if "Expected end of definition" in str(e):
            pytest.fail("UDL support not implemented: complex UDL case fails with 'Expected end of definition' error")
        else:
            raise e


def test_user_defined_literals_various_patterns():
    """Test various UDL suffix patterns - all should work after fix.""" 
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    test_cases = [
        "int a = 1.5fubar;",
        "int b = 42ulbar;", 
        "int c = 3.14159q_pi;",
        "int d = 0xFFq_hex;"
    ]
    
    for input_text in test_cases:
        parser = DefinitionParser(input_text, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        
        try:
            ast = parser.parse_declaration('member', 'member')
            parser.assert_end()
            assert ast is not None
        except DefinitionError as e:
            if "Expected end of definition" in str(e):
                pytest.fail(f"UDL support not implemented: fails with 'Expected end of definition' on '{input_text}'")
            else:
                raise e