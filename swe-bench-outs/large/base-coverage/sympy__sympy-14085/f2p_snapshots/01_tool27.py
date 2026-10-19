"""
Test for the Greek letter parsing issue in sympify.

This test ensures that sympify can properly parse Unicode Greek letters
like 'α' (alpha) without raising NameError.
"""

from sympy import sympify

def test_greek_letter_sympify_no_error():
    """Test that sympify does not raise NameError for Greek letters."""
    # This should work but previously raised NameError
    try:
        result = sympify("α")
        # If we get here without exception, it's working
        assert result is not None
    except NameError as e:
        # This is the error we're trying to fix
        raise AssertionError("sympify('α') should not raise NameError: %s" % str(e))

def test_greek_letter_expression_works():
    """Test that Greek letters work in expressions."""
    # Test that we can parse expressions with Greek letters
    try:
        result = sympify("α + β")
        # Should not raise an error and should produce a valid expression
        assert result is not None
    except NameError as e:
        raise AssertionError("sympify('α + β') should not raise NameError: %s" % str(e))

def test_greek_letter_basic_functionality():
    """Test basic functionality of Greek letter parsing."""
    # The main issue is that this should not fail with NameError
    try:
        # Test a few Greek letters
        letters = ["α", "β", "γ", "δ", "ε"]
        for letter in letters:
            result = sympify(letter)
            # Just make sure it doesn't raise NameError
            assert result is not None
    except NameError as e:
        raise AssertionError("Greek letter parsing should not raise NameError: %s" % str(e))