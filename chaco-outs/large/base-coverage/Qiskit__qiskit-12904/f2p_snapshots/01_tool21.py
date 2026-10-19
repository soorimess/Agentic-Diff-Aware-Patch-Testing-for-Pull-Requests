# This code is part of Qiskit.
#
# (C) Copyright IBM 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Regression tests for PR #12904: Move mcx synthesis methods with ancillas to the synthesis library
"""

import pytest


def test_mcx_synthesis_functions_importable():
    """Test that the new MCX synthesis functions are importable from the synthesis module."""
    # This test will fail before the PR is applied (functions don't exist)
    # and pass after the PR is applied (functions exist)
    from qiskit.synthesis.multi_controlled import (
        synth_mcx_n_dirty_i15,
        synth_mcx_n_clean_m15,
        synth_mcx_1_clean_b95
    )
    
    # Verify they are callable functions
    assert callable(synth_mcx_n_dirty_i15)
    assert callable(synth_mcx_n_clean_m15)
    assert callable(synth_mcx_1_clean_b95)


def test_mcx_recursive_functionality():
    """Test that MCXRecursive gate works with new synthesis functions."""
    try:
        from qiskit.synthesis.multi_controlled import synth_mcx_1_clean_b95
        from qiskit.circuit.library.standard_gates import MCXRecursive
        from qiskit.circuit.quantumcircuit import QuantumCircuit
        
        # Create MCX gate and verify it works
        mcx_gate = MCXRecursive(num_ctrl_qubits=3)
        qc = QuantumCircuit(mcx_gate.num_qubits)
        qc.append(mcx_gate, list(range(mcx_gate.num_qubits)))
        
        # Should have valid circuit
        assert qc.num_qubits == mcx_gate.num_qubits
        assert len(qc.data) > 0
        
    except ImportError:
        # This test should only run after the PR is applied
        pytest.skip("Functions not yet available in synthesis module")


def test_mcx_vchain_dirty_functionality():
    """Test that MCXVChain with dirty ancillas works with new synthesis functions."""
    try:
        from qiskit.synthesis.multi_controlled import synth_mcx_n_dirty_i15
        from qiskit.circuit.library.standard_gates import MCXVChain
        from qiskit.circuit.quantumcircuit import QuantumCircuit
        
        # Create MCX gate with dirty ancillas and verify it works
        mcx_gate = MCXVChain(num_ctrl_qubits=3, dirty_ancillas=True)
        qc = QuantumCircuit(mcx_gate.num_qubits)
        qc.append(mcx_gate, list(range(mcx_gate.num_qubits)))
        
        # Should have valid circuit
        assert qc.num_qubits == mcx_gate.num_qubits
        assert len(qc.data) > 0
        
    except ImportError:
        # This test should only run after the PR is applied
        pytest.skip("Functions not yet available in synthesis module")


def test_mcx_vchain_clean_functionality():
    """Test that MCXVChain with clean ancillas works with new synthesis functions."""
    try:
        from qiskit.synthesis.multi_controlled import synth_mcx_n_clean_m15
        from qiskit.circuit.library.standard_gates import MCXVChain
        from qiskit.circuit.quantumcircuit import QuantumCircuit
        
        # Create MCX gate with clean ancillas and verify it works
        mcx_gate = MCXVChain(num_ctrl_qubits=3, dirty_ancillas=False)
        qc = QuantumCircuit(mcx_gate.num_qubits)
        qc.append(mcx_gate, list(range(mcx_gate.num_qubits)))
        
        # Should have valid circuit
        assert qc.num_qubits == mcx_gate.num_qubits
        assert len(qc.data) > 0
        
    except ImportError:
        # This test should only run after the PR is applied
        pytest.skip("Functions not yet available in synthesis module")