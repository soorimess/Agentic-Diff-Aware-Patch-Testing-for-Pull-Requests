"""Test for the issue with sympify(u"α") not working."""

def test_greek_letter_sympify():
    """Test that greek letters can be parsed by sympify."""
    from sympy import sympify
    # The main issue: sympify(u"α") raised NameError: name 'α' is not defined
    # This test ensures that the specific error condition is fixed
    result = sympify(u"α")
    # If we get here without NameError, the fix works
    assert result is not None