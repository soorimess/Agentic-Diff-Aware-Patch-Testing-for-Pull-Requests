"""
Test for the Greek letter parsing issue in sympify.

This test ensures that sympify can properly parse Unicode Greek letters
like 'α' (alpha) without raising NameError, which was the core issue reported.
"""

from sympy import sympify

def test_greek_letter_sympify_no_nameerror():
    """
    Test that sympify does not raise NameError for Greek letters.
    
    This addresses the issue where sympify(u"α") would raise:
    NameError: name 'α' is not defined
    
    The fix ensures that Unicode Greek letters can be parsed as symbols.
    """
    # This should work without raising NameError
    try:
        result = sympify("α")
        # If we get here without exception, the issue is fixed
        assert result is not None
    except NameError as e:
        raise AssertionError("sympify('α') should not raise NameError: %s" % str(e))

def test_greek_letters_in_expressions():
    """
    Test that Greek letters work in mathematical expressions.
    
    This ensures that the parsing works not just for single letters,
    but also in expressions like "α + β".
    """
    try:
        result = sympify("α + β")
        # Should not raise an error
        assert result is not None
    except NameError as e:
        raise AssertionError("sympify('α + β') should not raise NameError: %s" % str(e))

def test_multiple_greek_letters():
    """
    Test that multiple Greek letters can be parsed.
    
    This tests the general robustness of Greek letter parsing.
    """
    try:
        letters = ["α", "β", "γ", "δ", "ε"]
        for letter in letters:
            result = sympify(letter)
            assert result is not None
    except NameError as e:
        raise AssertionError("Greek letter parsing should not raise NameError: %s" % str(e))