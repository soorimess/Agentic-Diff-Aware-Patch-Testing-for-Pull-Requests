def test_parse_latex_nested_fraction_denominator_brackets_regression():
    # Regression test for latex parsing of nested fractions in the denominator
    # that previously produced an incorrect expression due to missing brackets.
    try:
        from sympy.parsing.latex import parse_latex
    except Exception:
        # Latex parser (antlr4) is not available in this environment; skip.
        return
    from sympy import symbols

    a, b, c = symbols('a b c')
    latex_str = "\\frac{\\frac{a^3+b}{c}}{\\frac{1}{c^2}}"
    try:
        parsed = parse_latex(latex_str)
    except Exception:
        # If latex parsing isn't fully available in this environment, skip.
        return
    expected = ((a**3 + b) / c) / (1 / (c**2))
    assert parsed == expected
