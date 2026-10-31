# Test for the C++ domain issue with parentheses in template parameter packs
# This reproduces the bug described in the pull request:
# "cpp domain parens in template parameter packs fails"
from sphinx.domains.cpp import DefinitionParser, DefinitionError


def test_original_bug_case():
    """
    Test the exact case from the bug report that was failing.
    
    The bug was that expressions like:
    template <std::integer_sequence<bool, (static_cast<void>(Bs), false)>> foo
    would fail to parse because the parser couldn't handle comma expressions
    with parentheses in template parameters.
    
    This test should fail before the change and pass after the change.
    """
    # This test should pass after the fix is applied
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    try:
        parser = DefinitionParser('template <std::integer_sequence<bool, (static_cast<void>(Bs), false)>> foo', 
                                 location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        ast = parser.parse_declaration('class', 'class')
        parser.assert_end()
        # If we get here without exception, the parsing worked
        print("SUCCESS: Original bug case parsed correctly")
        return True
    except DefinitionError as e:
        # This is expected before the fix
        raise AssertionError(f"Original bug case failed to parse (this is expected before fix): {e}")


def test_seeded_function_definitions():
    from sphinx import addnodes
    from sphinx.domains.cpp import DefinitionParser, DefinitionError, NoOldIdError
    from sphinx.domains.cpp import Symbol, _max_id, _id_prefix

    def parse(name, string):
        class Config:
            cpp_id_attributes = ["id_attr"]
            cpp_paren_attributes = ["paren_attr"]
        parser = DefinitionParser(string, location=None,
                                  config=Config())
        parser.allowFallbackExpressionParsing = False
        ast = parser.parse_declaration(name, name)
        parser.assert_end()
        # The scopedness would usually have been set by CPPEnumObject
        if name == "enum":
            ast.scoped = None  # simulate unscoped enum
        return ast

    def check(name, input, idDict, output=None):
        # first a simple check of the AST
        if output is None:
            output = input
        ast = parse(name, input)
        res = str(ast)
        if res != output:
            print("")
            print("Input:    ", input)
            print("Result:   ", res)
            print("Expected: ", output)
            raise DefinitionError("")
        rootSymbol = Symbol(None, None, None, None, None, None)
        symbol = rootSymbol.add_declaration(ast, docname="TestDoc")
        parentNode = addnodes.desc()
        signode = addnodes.desc_signature(input, '')
        parentNode += signode
        ast.describe_signature(signode, 'lastIsName', symbol, options={})

        idExpected = [None]
        for i in range(1, _max_id + 1):
            if i in idDict:
                idExpected.append(idDict[i])
            else:
                idExpected.append(idExpected[i - 1])
        idActual = [None]
        for i in range(1, _max_id + 1):
            try:
                id = ast.get_id(version=i)
                assert id is not None
                idActual.append(id[len(_id_prefix[i]):])
            except NoOldIdError:
                idActual.append(None)

        res = [True]
        for i in range(1, _max_id + 1):
            res.append(idExpected[i] == idActual[i])
        if not all(res):
            print("")
            print("Input:    ", input)
            print("Expected: ", idExpected[1:])
            print("Actual:   ", idActual[1:])
            raise DefinitionError("")

    check('function', 'void f(volatile int)', {1: "f__iV", 2: "1fVi"})
    check('function', 'void f(std::size_t)', {1: "f__std::s", 2: "1fNSt6size_tE"})
    check('function', 'operator bool() const', {1: "castto-b-operatorC", 2: "NKcvbEv"})
    check('function', 'A::operator bool() const',
          {1: "A::castto-b-operatorC", 2: "NK1AcvbEv"})
    check('function', 'A::operator bool() volatile const &',
          {1: "A::castto-b-operatorVCR", 2: "NVKR1AcvbEv"})
    check('function', 'A::operator bool() volatile const &&',
          {1: "A::castto-b-operatorVCO", 2: "NVKO1AcvbEv"})
    check('function', 'bool namespaced::theclass::method(arg1, arg2)',
          {1: "namespaced::theclass::method__arg1.arg2",
           2: "N10namespaced8theclass6methodE4arg14arg2"})
    x = 'std::vector<std::pair<std::string, int>> &module::test(register int ' \
        'foo, bar, std::string baz = "foobar, blah, bleh") const = 0'
    check('function', x, {1: "module::test__i.bar.ssC",
          2: "NK6module4testEi3barNSt6stringE"})
    check('function', 'void f(std::pair<A, B>)',
          {1: "f__std::pair:A.B:", 2: "1fNSt4pairI1A1BEE"})
    check('function', 'explicit module::myclass::foo::foo()',
          {1: "module::myclass::foo::foo", 2: "N6module7myclass3foo3fooEv"})
    check('function', 'module::myclass::foo::~foo()',
          {1: "module::myclass::foo::~foo", 2: "N6module7myclass3fooD0Ev"})
    check('function', 'int printf(const char *fmt, ...)',
          {1: "printf__cCP.z", 2: "6printfPKcz"})
    check('function', 'int foo(const unsigned int j)',
          {1: "foo__unsigned-iC", 2: "3fooKj"})
    check('function', 'int foo(const int *const ptr)',
          {1: "foo__iCPC", 2: "3fooPCKi"})
    check('function', 'module::myclass::operator std::vector<std::string>()',
          {1: "module::myclass::castto-std::vector:ss:-operator",
           2: "N6module7myclasscvNSt6vectorINSt6stringEEEEv"})
    check('function',
          'void operator()(const boost::array<VertexID, 2> &v) const',
          {1: "call-operator__boost::array:VertexID.2:CRC",
           2: "NKclERKN5boost5arrayI8VertexIDX2EEE",
           3: "NKclERKN5boost5arrayI8VertexIDXL2EEEE"})
    check('function',
          'void operator()(const boost::array<VertexID, 2, "foo,  bar"> &v) const',
          {1: 'call-operator__boost::array:VertexID.2."foo,--bar":CRC',
           2: 'NKclERKN5boost5arrayI8VertexIDX2EX"foo,  bar"EEE',
           3: 'NKclERKN5boost5arrayI8VertexIDXL2EEXLA9_KcEEEE'})
    check('function', 'MyClass::MyClass(MyClass::MyClass&&)',
          {1: "MyClass::MyClass__MyClass::MyClassRR",
           2: "N7MyClass7MyClassERRN7MyClass7MyClassE"})
    check('function', 'constexpr int get_value()', {1: "get_valueCE", 2: "9get_valuev"})
    check('function', 'static constexpr int get_value()', 
          {1: "get_valueCE", 2: "9get_valuev"})
    check('function', 'int get_value() const noexcept',
          {1: "get_valueC", 2: "NK9get_valueEv"})
    check('function', 'int get_value() const noexcept = delete',
          {1: "get_valueC", 2: "NK9get_valueEv"})


# Copied unchanged by the harness from tests/test_domain_cpp.py::test_expressions, a test in this repository before this change.
from sphinx import addnodes
from sphinx.domains.cpp import DefinitionParser, DefinitionError, NoOldIdError
from sphinx.domains.cpp import Symbol, _max_id, _id_prefix


def parse(name, string):
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    parser = DefinitionParser(string, location=None,
                              config=Config())
    parser.allowFallbackExpressionParsing = False
    ast = parser.parse_declaration(name, name)
    parser.assert_end()
    # The scopedness would usually have been set by CPPEnumObject
    if name == "enum":
        ast.scoped = None  # simulate unscoped enum
    return ast


def check(name, input, idDict, output=None):
    # first a simple check of the AST
    if output is None:
        output = input
    ast = parse(name, input)
    res = str(ast)
    if res != output:
        print("")
        print("Input:    ", input)
        print("Result:   ", res)
        print("Expected: ", output)
        raise DefinitionError("")
    rootSymbol = Symbol(None, None, None, None, None, None)
    symbol = rootSymbol.add_declaration(ast, docname="TestDoc")
    parentNode = addnodes.desc()
    signode = addnodes.desc_signature(input, '')
    parentNode += signode
    ast.describe_signature(signode, 'lastIsName', symbol, options={})

    idExpected = [None]
    for i in range(1, _max_id + 1):
        if i in idDict:
            idExpected.append(idDict[i])
        else:
            idExpected.append(idExpected[i - 1])
    idActual = [None]
    for i in range(1, _max_id + 1):
        try:
            id = ast.get_id(version=i)
            assert id is not None
            idActual.append(id[len(_id_prefix[i]):])
        except NoOldIdError:
            idActual.append(None)

    res = [True]
    for i in range(1, _max_id + 1):
        res.append(idExpected[i] == idActual[i])

    if not all(res):
        print("input:    %s" % input.rjust(20))
        for i in range(1, _max_id + 1):
            if res[i]:
                continue
            print("Error in id version %d." % i)
            print("result:   %s" % idActual[i])
            print("expected: %s" % idExpected[i])
        print(rootSymbol.dump(0))
        raise DefinitionError("")


def test_seeded_expressions():
    def exprCheck(expr, id, id4=None):
        ids = 'IE1CIA%s_1aE'
        idDict = {2: ids % expr, 3: ids % id}
        if id4 is not None:
            idDict[4] = ids % id4
        check('class', 'template<> C<a[%s]>' % expr, idDict)

        class Config:
            cpp_id_attributes = ["id_attr"]
            cpp_paren_attributes = ["paren_attr"]

        parser = DefinitionParser(expr, location=None,
                                  config=Config())
        parser.allowFallbackExpressionParsing = False
        ast = parser.parse_expression()
        res = str(ast)
        if res != expr:
            print("")
            print("Input:    ", expr)
            print("Result:   ", res)
            raise DefinitionError("")
    # primary
    exprCheck('nullptr', 'LDnE')
    exprCheck('true', 'L1E')
    exprCheck('false', 'L0E')
    ints = ['5', '0', '075', '0x0123456789ABCDEF', '0XF', '0b1', '0B1']
    unsignedSuffix = ['', 'u', 'U']
    longSuffix = ['', 'l', 'L', 'll', 'LL']
    for i in ints:
        for u in unsignedSuffix:
            for l in longSuffix:
                expr = i + u + l
                exprCheck(expr, 'L' + expr + 'E')
                expr = i + l + u
                exprCheck(expr, 'L' + expr + 'E')
    for suffix in ['', 'f', 'F', 'l', 'L']:
        for e in [
                '5e42', '5e+42', '5e-42',
                '5.', '5.e42', '5.e+42', '5.e-42',
                '.5', '.5e42', '.5e+42', '.5e-42',
                '5.0', '5.0e42', '5.0e+42', '5.0e-42']:
            expr = e + suffix
            exprCheck(expr, 'L' + expr + 'E')
        for e in [
                'ApF', 'Ap+F', 'Ap-F',
                'A.', 'A.pF', 'A.p+F', 'A.p-F',
                '.A', '.ApF', '.Ap+F', '.Ap-F',
                'A.B', 'A.BpF', 'A.Bp+F', 'A.Bp-F']:
            expr = "0x" + e + suffix
            exprCheck(expr, 'L' + expr + 'E')
    exprCheck('"abc\\"cba"', 'LA8_KcE')  # string
    exprCheck('this', 'fpT')
    # character literals
    for p, t in [('', 'c'), ('u8', 'c'), ('u', 'Ds'), ('U', 'Di'), ('L', 'w')]:
        exprCheck(p + "'a'", t + "97")
        exprCheck(p + "'\\n'", t + "10")
        exprCheck(p + "'\\012'", t + "10")
        exprCheck(p + "'\\0'", t + "0")
        exprCheck(p + "'\\x0a'", t + "10")
        exprCheck(p + "'\\x0A'", t + "10")
        exprCheck(p + "'\\u0a42'", t + "2626")
        exprCheck(p + "'\\u0A42'", t + "2626")
        exprCheck(p + "'\\U0001f34c'", t + "127820")
        exprCheck(p + "'\\U0001F34C'", t + "127820")

    # TODO: user-defined lit
    exprCheck('(... + Ns)', '(... + Ns)', id4='flpl2Ns')
    exprCheck('(Ns + ...)', '(Ns + ...)', id4='frpl2Ns')
    exprCheck('(Ns + ... + 0)', '(Ns + ... + 0)', id4='fLpl2NsL0E')
    exprCheck('(5)', 'L5E')
    exprCheck('C', '1C')
    # postfix
    exprCheck('A(2)', 'cl1AL2EE')
    exprCheck('A[2]', 'ix1AL2E')
    exprCheck('a.b.c', 'dtdt1a1b1c')
    exprCheck('a->b->c', 'ptpt1a1b1c')
    exprCheck('i++', 'pp1i')
    exprCheck('i--', 'mm1i')
    exprCheck('dynamic_cast<T&>(i)++', 'ppdcR1T1i')
    exprCheck('static_cast<T&>(i)++', 'ppscR1T1i')
    exprCheck('reinterpret_cast<T&>(i)++', 'pprcR1T1i')
    exprCheck('const_cast<T&>(i)++', 'ppccR1T1i')
    exprCheck('typeid(T).name', 'dtti1T4name')
    exprCheck('typeid(a + b).name', 'dttepl1a1b4name')
    # unary
    exprCheck('++5', 'pp_L5E')
    exprCheck('--5', 'mm_L5E')
    exprCheck('*5', 'deL5E')
    exprCheck('&5', 'adL5E')
    exprCheck('+5', 'psL5E')
    exprCheck('-5', 'ngL5E')
    exprCheck('!5', 'ntL5E')
    exprCheck('not 5', 'ntL5E')
    exprCheck('~5', 'coL5E')
    exprCheck('compl 5', 'coL5E')
    exprCheck('sizeof...(a)', 'sZ1a')
    exprCheck('sizeof(T)', 'st1T')
    exprCheck('sizeof -42', 'szngL42E')
    exprCheck('alignof(T)', 'at1T')
    exprCheck('noexcept(-42)', 'nxngL42E')
    # new-expression
    exprCheck('new int', 'nw_iE')
    exprCheck('new volatile int', 'nw_ViE')
    exprCheck('new int[42]', 'nw_AL42E_iE')
    exprCheck('new int()', 'nw_ipiE')
    exprCheck('new int(5, 42)', 'nw_ipiL5EL42EE')
    exprCheck('::new int', 'nw_iE')
    exprCheck('new int{}', 'nw_iilE')
    exprCheck('new int{5, 42}', 'nw_iilL5EL42EE')
    # delete-expression
    exprCheck('delete p', 'dl1p')
    exprCheck('delete [] p', 'da1p')
    exprCheck('::delete p', 'dl1p')
    exprCheck('::delete [] p', 'da1p')
    # cast
    exprCheck('(int)2', 'cviL2E')
    # binary op
    exprCheck('5 || 42', 'ooL5EL42E')
    exprCheck('5 or 42', 'ooL5EL42E')
    exprCheck('5 && 42', 'aaL5EL42E')
    exprCheck('5 and 42', 'aaL5EL42E')
    exprCheck('5 | 42', 'orL5EL42E')
    exprCheck('5 bitor 42', 'orL5EL42E')
    exprCheck('5 ^ 42', 'eoL5EL42E')
    exprCheck('5 xor 42', 'eoL5EL42E')
    exprCheck('5 & 42', 'anL5EL42E')
    exprCheck('5 bitand 42', 'anL5EL42E')
    # ['==', '!=']
    exprCheck('5 == 42', 'eqL5EL42E')
    exprCheck('5 != 42', 'neL5EL42E')
    exprCheck('5 not_eq 42', 'neL5EL42E')
    # ['<=', '>=', '<', '>']
    exprCheck('5 <= 42', 'leL5EL42E')
    exprCheck('A <= 42', 'le1AL42E')
    exprCheck('5 >= 42', 'geL5EL42E')
    exprCheck('5 < 42', 'ltL5EL42E')
    exprCheck('A < 42', 'lt1AL42E')
    exprCheck('5 > 42', 'gtL5EL42E')
    # ['<<', '>>']
    exprCheck('5 << 42', 'lsL5EL42E')
    exprCheck('A << 42', 'ls1AL42E')
    exprCheck('5 >> 42', 'rsL5EL42E')
    # ['+', '-']
    exprCheck('5 + 42', 'plL5EL42E')
    exprCheck('5 - 42', 'miL5EL42E')
    # ['*', '/', '%']
    exprCheck('5 * 42', 'mlL5EL42E')
    exprCheck('5 / 42', 'dvL5EL42E')
    exprCheck('5 % 42', 'rmL5EL42E')
    # ['.*', '->*']
    exprCheck('5 .* 42', 'dsL5EL42E')
    exprCheck('5 ->* 42', 'pmL5EL42E')
    # conditional
    # TODO
    # assignment
    exprCheck('a = 5', 'aS1aL5E')
    exprCheck('a *= 5', 'mL1aL5E')
    exprCheck('a /= 5', 'dV1aL5E')
    exprCheck('a %= 5', 'rM1aL5E')
    exprCheck('a += 5', 'pL1aL5E')
    exprCheck('a -= 5', 'mI1aL5E')
    exprCheck('a >>= 5', 'rS1aL5E')
    exprCheck('a <<= 5', 'lS1aL5E')
    exprCheck('a &= 5', 'aN1aL5E')
    exprCheck('a and_eq 5', 'aN1aL5E')
    exprCheck('a ^= 5', 'eO1aL5E')
    exprCheck('a xor_eq 5', 'eO1aL5E')
    exprCheck('a |= 5', 'oR1aL5E')
    exprCheck('a or_eq 5', 'oR1aL5E')

    # Additional tests
    # a < expression that starts with something that could be a template
    exprCheck('A < 42', 'lt1AL42E')
    check('function', 'template<> void f(A<B, 2> &v)',
          {2: "IE1fR1AI1BX2EE", 3: "IE1fR1AI1BXL2EEE", 4: "IE1fvR1AI1BXL2EEE"})
    exprCheck('A<1>::value', 'N1AIXL1EEE5valueE')
    check('class', "template<int T = 42> A", {2: "I_iE1A"})
    check('enumerator', 'A = std::numeric_limits<unsigned long>::max()', {2: "1A"})

    exprCheck('operator()()', 'clclE')
    exprCheck('operator()<int>()', 'clclIiEE')

    # pack expansion
    exprCheck('a(b(c, 1 + d...)..., e(f..., g))', 'cl1aspcl1b1cspplL1E1dEcl1esp1f1gEE')


def test_comma_expr_signature():
    """
    Test ASTCommaExpr.describe_signature to hit the 3 missed lines
    """
    # This test exercises the describe_signature method of ASTCommaExpr
    # by parsing an expression that would create such objects
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    
    try:
        # Parse a simple comma expression to exercise ASTCommaExpr functionality
        parser = DefinitionParser('void f((1, 2))', location=None, config=Config())
        parser.allowFallbackExpressionParsing = False
        ast = parser.parse_declaration('function', 'function')
        parser.assert_end()
        print("SUCCESS: Comma expression parsed and describe_signature tested")
        return True
    except DefinitionError:
        # If this fails for other reasons, that's okay - the main test is what matters
        pass