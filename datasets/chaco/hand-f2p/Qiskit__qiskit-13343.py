import pytest

from qiskit.qasm3 import ast


NODES = [
    lambda: ast.Identifier("q"),
    lambda: ast.IntegerLiteral(3),
    lambda: ast.Include("stdgates.inc"),
    lambda: ast.QuantumDeclaration(ast.Identifier("q")),
]


@pytest.mark.parametrize("make", NODES)
def test_ast_nodes_are_slotted(make):
    # The exporter builds many of these; they carry no per-instance __dict__.
    node = make()
    assert not hasattr(node, "__dict__")
    with pytest.raises(AttributeError):
        node.not_a_field = 1
