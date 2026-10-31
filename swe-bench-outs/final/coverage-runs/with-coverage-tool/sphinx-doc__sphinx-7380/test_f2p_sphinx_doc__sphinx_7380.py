# Test for the specific issue with parentheses in template parameter packs
# This test verifies the core functionality that was added in the pull request

from sphinx.domains.cpp import DefinitionParser, DefinitionError, NoOldIdError
from sphinx.domains.cpp import Symbol, _max_id, _id_prefix
from sphinx import addnodes


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
        print("ID Expected:", idExpected[1:])
        print("ID Actual:  ", idActual[1:])
        raise DefinitionError("")


def test_comma_expressions_directly():
    """Test that comma expressions can be parsed directly.
    
    This tests the core functionality that was added in the fix - 
    parsing comma expressions like (a, b) correctly.
    """
    # Test parsing a comma expression directly - this should work after the fix
    class Config:
        cpp_id_attributes = ["id_attr"]
        cpp_paren_attributes = ["paren_attr"]
    parser = DefinitionParser('(a, b)', location=None,
                              config=Config())
    parser.allowFallbackExpressionParsing = False
    ast = parser.parse_expression()
    # This should return an ASTCommaExpr object, not fail
    assert str(ast) == '(a, b)'


def test_initializers():
    """Test braced init list functionality.
    
    This test exercises the ASTBracedInitList.describe_signature function
    that was added in the pull request.
    """
    # Test simple braced init list
    check('member', 'T v = {}', {1: 'v__T', 2: '1v'})
    
    # Test braced init list with content
    check('member', 'T v = {42, 42, 42}', {1: 'v__T', 2: '1v'})


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


# Copied unchanged by the harness from tests/test_domain_cpp.py::test_function_definitions, a test in this repository before this change.
import pytest
from sphinx import addnodes
from sphinx.domains.cpp import DefinitionParser, DefinitionError, NoOldIdError
from sphinx.domains.cpp import Symbol, _max_id, _id_prefix


def test_seeded_function_definitions():
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
    check('function', 'int get_value() volatile const',
          {1: "get_valueVC", 2: "NVK9get_valueEv"})
    check('function', 'MyClass::MyClass(MyClass::MyClass&&) = default',
          {1: "MyClass::MyClass__MyClass::MyClassRR",
           2: "N7MyClass7MyClassERRN7MyClass7MyClassE"})
    check('function', 'virtual MyClass::a_virtual_function() const override',
          {1: "MyClass::a_virtual_functionC", 2: "NK7MyClass18a_virtual_functionEv"})
    check('function', 'A B() override', {1: "B", 2: "1Bv"})
    check('function', 'A B() final', {1: "B", 2: "1Bv"})
    check('function', 'A B() final override', {1: "B", 2: "1Bv"})
    check('function', 'A B() override final', {1: "B", 2: "1Bv"},
          output='A B() final override')
    check('function', 'MyClass::a_member_function() volatile',
          {1: "MyClass::a_member_functionV", 2: "NV7MyClass17a_member_functionEv"})
    check('function', 'MyClass::a_member_function() volatile const',
          {1: "MyClass::a_member_functionVC", 2: "NVK7MyClass17a_member_functionEv"})
    check('function', 'MyClass::a_member_function() &&',
          {1: "MyClass::a_member_functionO", 2: "NO7MyClass17a_member_functionEv"})
    check('function', 'MyClass::a_member_function() &',
          {1: "MyClass::a_member_functionR", 2: "NR7MyClass17a_member_functionEv"})
    check('function', 'MyClass::a_member_function() const &',
          {1: "MyClass::a_member_functionCR", 2: "NKR7MyClass17a_member_functionEv"})
    check('function', 'int main(int argc, char *argv[])',
          {1: "main__i.cPA", 2: "4mainiA_Pc"})
    check('function', 'MyClass &MyClass::operator++()',
          {1: "MyClass::inc-operator", 2: "N7MyClassppEv"})
    check('function', 'MyClass::pointer MyClass::operator->()',
          {1: "MyClass::pointer-operator", 2: "N7MyClassptEv"})

    x = 'std::vector<std::pair<std::string, int>> &module::test(register int ' \
        'foo, bar[n], std::string baz = "foobar, blah, bleh") const = 0'
    check('function', x, {1: "module::test__i.barA.ssC",
                          2: "NK6module4testEiAn_3barNSt6stringE",
                          3: "NK6module4testEiA1n_3barNSt6stringE"})
    check('function',
          'int foo(Foo f = Foo(double(), std::make_pair(int(2), double(3.4))))',
          {1: "foo__Foo", 2: "3foo3Foo"})
    check('function', 'int foo(A a = x(a))', {1: "foo__A", 2: "3foo1A"})
    with pytest.raises(DefinitionError):
        parse('function', 'int foo(B b=x(a)')
    with pytest.raises(DefinitionError):
        parse('function', 'int foo)C c=x(a))')
    with pytest.raises(DefinitionError):
        parse('function', 'int foo(D d=x(a')
    check('function', 'int foo(const A&... a)', {1: "foo__ACRDp", 2: "3fooDpRK1A"})
    check('function', 'int foo(const A&...)', {1: "foo__ACRDp", 2: "3fooDpRK1A"})
    check('function', 'int foo(const A*... a)', {1: "foo__ACPDp", 2: "3fooDpPK1A"})
    check('function', 'int foo(const A*...)', {1: "foo__ACPDp", 2: "3fooDpPK1A"})
    check('function', 'int foo(const int A::*... a)', {2: "3fooDpM1AKi"})
    check('function', 'int foo(const int A::*...)', {2: "3fooDpM1AKi"})
    #check('function', 'int foo(int (*a)(A)...)', {1: "foo__ACRDp", 2: "3fooDpPK1A"})
    #check('function', 'int foo(int (*)(A)...)', {1: "foo__ACRDp", 2: "3fooDpPK1A"})
    check('function', 'virtual void f()', {1: "f", 2: "1fv"})
    # test for ::nestedName, from issue 1738
    check("function", "result(int val, ::std::error_category const &cat)",
          {1: "result__i.std::error_categoryCR", 2: "6resultiRKNSt14error_categoryE"})
    check("function", "int *f()", {1: "f", 2: "1fv"})
    # tests derived from issue #1753 (skip to keep sanity)
    check("function", "f(int (&array)[10])", {2: "1fRA10_i", 3: "1fRAL10E_i"})
    check("function", "void f(int (&array)[10])", {2: "1fRA10_i", 3: "1fRAL10E_i"})
    check("function", "void f(float *q(double))", {2: "1fFPfdE"})
    check("function", "void f(float *(*q)(double))", {2: "1fPFPfdE"})
    check("function", "void f(float (*q)(double))", {2: "1fPFfdE"})
    check("function", "int (*f(double d))(float)", {1: "f__double", 2: "1fd"})
    check("function", "int (*f(bool b))[5]", {1: "f__b", 2: "1fb"})
    check("function", "int (*A::f(double d) const)(float)",
          {1: "A::f__doubleC", 2: "NK1A1fEd"})
    check("function", "void f(std::shared_ptr<int(double)> ptr)",
          {2: "1fNSt10shared_ptrIFidEEE"})
    check("function", "void f(int *const p)", {1: "f__iPC", 2: "1fPCi"})
    check("function", "void f(int *volatile const p)", {1: "f__iPVC", 2: "1fPVCi"})

    check('function', 'extern int f()', {1: 'f', 2: '1fv'})

    check('function', 'decltype(auto) f()', {1: 'f', 2: "1fv"})

    # TODO: make tests for functions in a template, e.g., Test<int&&()>
    # such that the id generation for function type types is correct.

    check('function', 'friend std::ostream &f(std::ostream &s, int i)',
          {1: 'f__osR.i', 2: '1fRNSt7ostreamEi'})

    # from breathe#223
    check('function', 'void f(struct E e)', {1: 'f__E', 2: '1f1E'})
    check('function', 'void f(class E e)', {1: 'f__E', 2: '1f1E'})
    check('function', 'void f(typename E e)', {1: 'f__E', 2: '1f1E'})
    check('function', 'void f(enum E e)', {1: 'f__E', 2: '1f1E'})
    check('function', 'void f(union E e)', {1: 'f__E', 2: '1f1E'})

    # pointer to member (function)
    check('function', 'void f(int C::*)', {2: '1fM1Ci'})
    check('function', 'void f(int C::* p)', {2: '1fM1Ci'})
    check('function', 'void f(int ::C::* p)', {2: '1fM1Ci'})
    check('function', 'void f(int C::*const)', {2: '1fKM1Ci'})
    check('function', 'void f(int C::*const&)', {2: '1fRKM1Ci'})
    check('function', 'void f(int C::*volatile)', {2: '1fVM1Ci'})
    check('function', 'void f(int C::*const volatile)', {2: '1fVKM1Ci'},
          output='void f(int C::*volatile const)')
    check('function', 'void f(int C::*volatile const)', {2: '1fVKM1Ci'})
    check('function', 'void f(int (C::*)(float, double))', {2: '1fM1CFifdE'})
    check('function', 'void f(int (C::* p)(float, double))', {2: '1fM1CFifdE'})
    check('function', 'void f(int (::C::* p)(float, double))', {2: '1fM1CFifdE'})
    check('function', 'void f(void (C::*)() const &)', {2: '1fM1CKRFvvE'})
    check('function', 'int C::* f(int, double)', {2: '1fid'})
    check('function', 'void f(int C::* *p)', {2: '1fPM1Ci'})
    check('function', 'void f(int C::**)', {2: '1fPM1Ci'})
    check('function', 'void f(int C::*const *p)', {2: '1fPKM1Ci'})
    check('function', 'void f(int C::*const*)', {2: '1fPKM1Ci'})

    # exceptions from return type mangling
    check('function', 'template<typename T> C()', {2: 'I0E1Cv'})
    check('function', 'template<typename T> operator int()', {1: None, 2: 'I0Ecviv'})


# Copied unchanged by the harness from tests/test_domain_cpp.py::test_class_definitions, a test in this repository before this change.
from sphinx import addnodes
from sphinx.domains.cpp import DefinitionParser, DefinitionError, NoOldIdError
from sphinx.domains.cpp import Symbol, _max_id, _id_prefix


def test_seeded_class_definitions():
    check('class', 'public A', {1: "A", 2: "1A"}, output='A')
    check('class', 'private A', {1: "A", 2: "1A"})
    check('class', 'A final', {1: 'A', 2: '1A'})

    # test bases
    check('class', 'A', {1: "A", 2: "1A"})
    check('class', 'A::B::C', {1: "A::B::C", 2: "N1A1B1CE"})
    check('class', 'A : B', {1: "A", 2: "1A"})
    check('class', 'A : private B', {1: "A", 2: "1A"})
    check('class', 'A : public B', {1: "A", 2: "1A"})
    check('class', 'A : B, C', {1: "A", 2: "1A"})
    check('class', 'A : B, protected C, D', {1: "A", 2: "1A"})
    check('class', 'A : virtual private B', {1: 'A', 2: '1A'}, output='A : private virtual B')
    check('class', 'A : private virtual B', {1: 'A', 2: '1A'})
    check('class', 'A : B, virtual C', {1: 'A', 2: '1A'})
    check('class', 'A : public virtual B', {1: 'A', 2: '1A'})
    check('class', 'A : B, C...', {1: 'A', 2: '1A'})
    check('class', 'A : B..., C', {1: 'A', 2: '1A'})

    # from #4094
    check('class', 'template<class, class = std::void_t<>> has_var', {2: 'I00E7has_var'})
    check('class', 'template<class T> has_var<T, std::void_t<decltype(&T::var)>>',
          {2: 'I0E7has_varI1TNSt6void_tIDTadN1T3varEEEEE'})
