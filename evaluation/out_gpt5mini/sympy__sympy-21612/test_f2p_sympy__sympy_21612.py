from sympy import symbols, Pow, Mul, Add


a, b, c = symbols('a b c')


def test_nested_frac_parentheses_strprinter():
    """Regression test for nested fraction printing (sympy#21612).

    This ensures that a fraction whose denominator is itself a fraction
    keeps the denominator grouped when printed. The problematic LaTeX
    is "\\frac{\\frac{a^3+b}{c}}{\\frac{1}{c^2}}" which was
    rendered as ``((a**3 + b)/c)/1/(c**2)`` (wrong) instead of
    ``((a**3 + b)/c)/(1/(c**2))`` (correct).

    The expression below mimics the structure produced by the LaTeX
    parser for that input: the inner denominator is ``1/(c**2)`` and the
    outer denominator is its inverse, so we construct a double-inversion
    and check the StrPrinter output.
    """
    top = Mul(Add(Pow(a, 3), b), Pow(c, -1, evaluate=False), evaluate=False)

    inner = Pow(c, 2, evaluate=False)
    inner_inv = Pow(inner, -1, evaluate=False)        # 1/(c**2)
    outer_inverse = Pow(inner_inv, -1, evaluate=False)  # 1/(1/(c**2))

    expr = Mul(top, outer_inverse, evaluate=False)

    # Before the fix this prints without grouping the denominator; after
    # the fix it should print with parentheses around the denominator:
    assert str(expr) == '((a**3 + b)/c)/(1/(c**2))'
