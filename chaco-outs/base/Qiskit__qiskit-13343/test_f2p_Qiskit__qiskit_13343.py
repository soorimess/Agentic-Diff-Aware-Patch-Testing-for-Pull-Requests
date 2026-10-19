# This code is part of Qiskit.
#
# (C) Copyright IBM 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test for regression of PR #13343 - Improve OpenQASM 3 exporter performance for hardware-like circuits."""

from math import pi
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.qasm3 import Exporter


def test_performance_scenario_hardware_like_circuits():
    """Test the main performance scenario: many singly parametric 1q gates.
    
    This validates the key performance improvement targeted by PR #13343.
    """
    # Create a circuit with many gates using the same parameter - the performance target
    param = Parameter("angle")
    
    circuit = QuantumCircuit(3)
    # Create many gates with the same parameter - this is the performance scenario
    for i in range(100):  # 100 gates to stress test the optimized path
        circuit.ry(param, i % 3)
    
    # Should export correctly and efficiently with performance improvements
    exporter = Exporter(disable_constants=False)
    qasm = exporter.dumps(circuit)
    
    # Validate the output
    assert "OPENQASM 3.0;" in qasm
    assert "angle" in qasm
    assert qasm.count("ry") == 100


def test_parameter_processing_logic():
    """Test parameter processing logic that was restructured in PR #13343.
    
    This validates the parameter handling changes for pi constants and gate calls.
    """
    # Create circuit with pi constants and parameters
    param = Parameter("theta")
    
    circuit = QuantumCircuit(2)
    circuit.u(pi/2, param, pi, 0)
    
    # Test with disable_constants=False (should preserve pi expressions)
    exporter_false = Exporter(disable_constants=False)
    qasm_false = exporter_false.dumps(circuit)
    
    # Test with disable_constants=True (should evaluate pi expressions)
    exporter_true = Exporter(disable_constants=True)
    qasm_true = exporter_true.dumps(circuit)
    
    # Both should work correctly
    assert "OPENQASM 3.0;" in qasm_false
    assert "OPENQASM 3.0;" in qasm_true
    
    # With disable_constants=False, should preserve pi expressions
    assert "pi/2" in qasm_false or "pi / 2" in qasm_false
    assert "theta" in qasm_false
    
    # With disable_constants=True, should evaluate pi expressions
    assert "1.5707963267948966" in qasm_true  # pi/2
    assert "3.141592653589793" in qasm_true   # pi


def test_gate_call_with_single_parameter():
    """Test gate calls with single parameters to ensure proper handling.
    
    This validates the gate call parameter processing logic changes.
    """
    param = Parameter("alpha")
    
    circuit = QuantumCircuit(2)
    circuit.rx(param, 0)  # Single parameter on qubit
    circuit.ry(param, 1)  # Same parameter on different qubit
    
    # Export should work without issues
    exporter = Exporter(disable_constants=False)
    qasm = exporter.dumps(circuit)
    
    # Should produce valid QASM
    assert "OPENQASM 3.0;" in qasm
    assert "alpha" in qasm
    assert "rx" in qasm
    assert "ry" in qasm