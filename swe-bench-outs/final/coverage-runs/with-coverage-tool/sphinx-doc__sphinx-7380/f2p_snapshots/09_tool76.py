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