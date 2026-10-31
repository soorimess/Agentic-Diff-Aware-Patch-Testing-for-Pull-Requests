def test_greek_letter_parsing():
    """Test that sympify('α') works correctly."""
    from sympy import sympify
    
    # This call should succeed without NameError
    # The fix ensures unicode greek letters are handled properly
    result = sympify("α")
    
    # Verify that we get a valid result (not None)
    # This shows the parsing worked correctly
    assert result is not None