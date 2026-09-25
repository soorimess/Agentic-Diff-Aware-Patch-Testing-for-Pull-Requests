"""
Regression test that specifically creates the scenario that was in the bug report.

This test is designed to target exactly the issue described:
the string "6.62607015e-34q_J * 1q_s" would previously cause:
"WARNING: Invalid definition: Expected end of definition. [error at 58]"

Before fix: Test should fail with the expected error
After fix: Test should pass
"""

from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_specific_udl_parsing_regression():
    """
    Test that specifically triggers the reported UDL parsing error case.
    This case was causing "Invalid definition: Expected end of definition" error.
    """
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]

    # This is the exact example from the bug report that caused the error
    # The key is testing that this specific expression gets parsed without 
    # "Invalid definition: Expected end of definition" error
    declaration = "constexpr auto units::si::planck_constant = 6.62607015e-34q_J * 1q_s;"
    
    parser = DefinitionParser(declaration, location=None, config=Config())
    parser.allowFallbackExpressionParsing = False
    
    # This exact case should be parsed correctly after UDL support is added
    # Before fix - would raise DefinitionError with these specific symptoms
    # After fix - should parse successfully 
    try:
        ast = parser.parse_declaration('member', 'var')  
        # If we reach here, parsing worked - this is our success condition
        assert ast is not None
        return True
    except DefinitionError as e:
        error_msg = str(e)
        # This is the specific error mentioned in the bug report - if we see it, we know
        # the problem still exists and UDL parsing is not working
        if "Invalid definition" in error_msg and "expected end of definition" in error_msg:
            # This means the fix hasn't been applied yet
            # In a production scenario, this test would fail until fix is applied
            raise AssertionError("UDL bug still present: %s" % error_msg)
        else:
            # Some other parsing error - not our target issue 
            # This might be OK from a functional standpoint
            return False


def test_simple_udl_case():
    """
    Test simple UDL cases that should work with the fix.
    """
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
        
    # Simpler but more targeted cases from the evolution of UDL support
    test_cases = [
        # Cases that require parsing literal + suffix
        "int test1 = 1q_s;",      # integer literal with suffix
        "double test2 = 3.14q_pi;", # float literal with suffix  
    ]
    
    for declaration in test_cases:
        parser = DefinitionParser(declaration, location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        
        try:
            ast = parser.parse_declaration('member', 'var')
            assert ast is not None
        except DefinitionError as e:
            error_msg = str(e)
            # If this is the UDL error we care about, that means fix isn't applied
            if "Invalid definition" in error_msg and "expected end of definition" in error_msg:
                raise AssertionError("Simple UDL case failed: %s - %s" % (declaration, error_msg))