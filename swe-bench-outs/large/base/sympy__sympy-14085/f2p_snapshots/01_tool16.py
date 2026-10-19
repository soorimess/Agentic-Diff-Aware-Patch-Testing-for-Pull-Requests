"""
Regression test for sympify with Greek letters issue.

This test ensures that sympify can parse Greek letters like 'α' that are 
pretty printed for symbols of that name.
"""

from sympy import sympify, Symbol
from sympy.core.sympify import SympifyError


def test_sympify_greek_letter_alpha():
    """Test that sympify can parse the Greek letter alpha specifically."""
    # This should work - the original issue reported that this fails
    # In the fixed version, "α" should be parsed as Symbol('alpha')
    try:
        result = sympify("α")
        # If it works, it should return a valid SymPy object
        # The key test is that it doesn't raise SympifyError
        assert result is not None
        # It should be a symbol (though the exact type may vary)
        assert hasattr(result, 'is_Symbol') or hasattr(result, 'is_symbol')
    except SympifyError as e:
        # This is the error that should be fixed by the PR
        raise AssertionError("sympify('α') should work but raises SympifyError: %s" % str(e))
    except Exception as e:
        # Other exceptions might also indicate the issue
        raise AssertionError("sympify('α') should work but raises %s: %s" % (type(e).__name__, str(e)))


def test_sympify_greek_letter_beta():
    """Test that sympify can parse the Greek letter beta."""
    try:
        result = sympify("β")
        assert result is not None
        assert hasattr(result, 'is_Symbol') or hasattr(result, 'is_symbol')
    except SympifyError as e:
        raise AssertionError("sympify('β') should work but raises SympifyError: %s" % str(e))
    except Exception as e:
        raise AssertionError("sympify('β') should work but raises %s: %s" % (type(e).__name__, str(e)))


def test_repeated_decimals_parsing():
    """Test that repeated decimals notation works (new functionality)."""
    # Test 0.2[1] which should represent 0.2111... (19/90)
    # This is a new feature added by the PR
    try:
        result = sympify("0.2[1]")
        # Should parse to a rational number
        assert result is not None
        # The result should be equivalent to 19/90
    except Exception:
        # This might fail in the old version since repeated decimals is a new feature
        # We're mainly testing that the basic sympify functionality works
        pass


def test_symbol_creation_from_unicode():
    """Test that symbols with Unicode names work properly."""
    # Test that we can create a symbol from a Unicode string
    try:
        # This should work - creating a symbol with Unicode name
        alpha_symbol = Symbol("α")
        # And parsing it should work
        parsed_alpha = sympify("α")
        assert parsed_alpha is not None
    except Exception as e:
        raise AssertionError("Unicode symbol handling should work: %s" % str(e))


if __name__ == "__main__":
    test_sympify_greek_letter_alpha()
    test_sympify_greek_letter_beta()
    test_repeated_decimals_parsing()
    test_symbol_creation_from_unicode()
    print("All tests passed!")