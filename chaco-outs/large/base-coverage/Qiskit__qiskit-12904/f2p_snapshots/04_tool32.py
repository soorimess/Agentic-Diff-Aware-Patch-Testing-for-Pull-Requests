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
from qiskit.circuit.quantumcircuit import QuantumCircuit


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


def test_mcx_synthesis_functions_return_valid_circuits():
    """Test that the new MCX synthesis functions return valid QuantumCircuits."""
    # This test will fail before the PR is applied (functions don't exist)
    # and pass after the PR is applied (functions exist and work)
    from qiskit.synthesis.multi_controlled import (
        synth_mcx_n_dirty_i15,
        synth_mcx_n_clean_m15,
        synth_mcx_1_clean_b95
    )
    
    # Test synth_mcx_n_dirty_i15 returns a valid circuit
    qc_dirty = synth_mcx_n_dirty_i15(num_ctrl_qubits=3)
    assert isinstance(qc_dirty, QuantumCircuit)
    assert qc_dirty.num_qubits >= 3  # Should have at least 3 qubits
    assert len(qc_dirty.data) > 0  # Should have operations
    
    # Test synth_mcx_n_clean_m15 returns a valid circuit  
    qc_clean = synth_mcx_n_clean_m15(num_ctrl_qubits=3)
    assert isinstance(qc_clean, QuantumCircuit)
    assert qc_clean.num_qubits >= 3  # Should have at least 3 qubits
    assert len(qc_clean.data) > 0  # Should have operations
    
    # Test synth_mcx_1_clean_b95 returns a valid circuit
    qc_recursive = synth_mcx_1_clean_b95(num_ctrl_qubits=3)
    assert isinstance(qc_recursive, QuantumCircuit)
    assert qc_recursive.num_qubits >= 3  # Should have at least 3 qubits
    assert len(qc_recursive.data) > 0  # Should have operations


def test_mcx_synthesis_functions_have_correct_properties():
    """Test that the new MCX synthesis functions have expected properties."""
    # This test will fail before the PR is applied (functions don't exist)
    # and pass after the PR is applied (functions exist and have expected behavior)
    from qiskit.synthesis.multi_controlled import (
        synth_mcx_n_dirty_i15,
        synth_mcx_n_clean_m15,
        synth_mcx_1_clean_b95
    )
    
    # Test that functions can be called with different parameters
    # synth_mcx_n_dirty_i15
    qc1 = synth_mcx_n_dirty_i15(num_ctrl_qubits=3)
    assert isinstance(qc1, QuantumCircuit)
    assert len(qc1.data) > 0
    
    qc2 = synth_mcx_n_dirty_i15(num_ctrl_qubits=4, relative_phase=True)
    assert isinstance(qc2, QuantumCircuit)
    assert len(qc2.data) > 0
    
    qc3 = synth_mcx_n_dirty_i15(num_ctrl_qubits=4, action_only=True)
    assert isinstance(qc3, QuantumCircuit)
    assert len(qc3.data) > 0
    
    # synth_mcx_n_clean_m15
    qc4 = synth_mcx_n_clean_m15(num_ctrl_qubits=3)
    assert isinstance(qc4, QuantumCircuit)
    assert len(qc4.data) > 0
    
    # synth_mcx_1_clean_b95
    qc5 = synth_mcx_1_clean_b95(num_ctrl_qubits=4)
    assert isinstance(qc5, QuantumCircuit)
    assert len(qc5.data) > 0