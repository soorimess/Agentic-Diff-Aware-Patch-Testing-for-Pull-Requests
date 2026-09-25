from sympy import Add, Mul, Pow, symbols


def test_str_parenthesizes_reciprocal_power_denominator():
    a, b, c = symbols('a b c')
    numerator = Mul(Add(a**3, b, evaluate=False), Pow(c, -1, evaluate=False),
            evaluate=False)
    denominator = Pow(Pow(c, 2, evaluate=False), -1, evaluate=False)
    expr = Mul(numerator, Pow(denominator, -1, evaluate=False),
            evaluate=False)

    assert str(expr) == "((a**3 + b)/c)/(1/(c**2))"
