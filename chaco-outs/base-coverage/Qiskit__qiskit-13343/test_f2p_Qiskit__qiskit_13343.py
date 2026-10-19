# This code is part of Qiskit.
#
# (C) Copyright IBM 2023.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Regression tests for PR #13343: Improve OpenQASM 3 exporter performance for hardware-like circuits."""

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.qasm3 import dumps


def test_many_singly_parametric_gates_scenario():
    """Test the specific performance scenario from PR #13343.
    
    PR #13343 improves performance for "circuits with many singly parametric 1q gates, 
    parametrised by a single Parameter expression". This test validates that such 
    circuits export correctly.
    """
    # Create parameter that will be used in many gates (the performance optimization target)
    param = Parameter("theta")
    
    # Create a circuit that represents the exact scenario mentioned in the PR
    # Many singly parametric 1q gates parametrised by a single Parameter expression
    circuit = QuantumCircuit(3)
    
    # Add many gates using the same parameter - this is the core performance scenario
    for i in range(25):  # Many gates to exercise the optimization
        qubit = i % 3
        # Use different single-qubit parametric gates to cover various code paths
        if i % 4 == 0:
            circuit.ry(param, qubit)
        elif i % 4 == 1:
            circuit.rz(param, qubit)
        elif i % 4 == 2:
            circuit.rx(param, qubit)
        else:
            circuit.rxx(param, qubit, (qubit + 1) % 3)
    
    # Export to QASM3 - should work efficiently with PR's performance improvements
    qasm_str = dumps(circuit)
    
    # Validate the export worked correctly
    assert "OPENQASM 3.0;" in qasm_str
    assert any(gate in qasm_str for gate in ["ry(", "rz(", "rx(", "rxx("])
    assert "theta" in qasm_str


def test_parametric_circuit_basic_functionality():
    """Test basic parametric circuit functionality that PR #13343 builds upon.
    
    Ensures that the core functionality for parameterized circuits works correctly
    after the changes in PR #13343.
    """
    # Test with single parameter
    theta = Parameter("theta")
    circuit = QuantumCircuit(1)
    circuit.rz(theta, 0)
    
    qasm_str = dumps(circuit)
    assert "OPENQASM 3.0;" in qasm_str
    assert "rz(" in qasm_str
    assert "theta" in qasm_str
    
    # Test with multiple parameters
    phi = Parameter("phi")
    circuit2 = QuantumCircuit(2)
    circuit2.ry(theta, 0)
    circuit2.rz(phi, 1)
    
    qasm_str2 = dumps(circuit2)
    assert "OPENQASM 3.0;" in qasm_str2
    assert "ry(" in qasm_str2
    assert "rz(" in qasm_str2
    assert "theta" in qasm_str2
    assert "phi" in qasm_str2