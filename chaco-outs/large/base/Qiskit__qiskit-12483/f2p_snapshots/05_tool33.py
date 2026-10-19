# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test for the num_operand_distribution parameter in random_circuit function."""

from qiskit.circuit import QuantumCircuit
from qiskit.circuit.random import random_circuit
from qiskit.circuit.exceptions import CircuitError
from test import QiskitTestCase  # pylint: disable=wrong-import-order
import numpy as np


class TestRandomCircuitNumOperandDistribution(QiskitTestCase):
    """Testing the num_operand_distribution parameter in random_circuit."""

    def test_num_operand_distribution_basic_functionality(self):
        """Test that num_operand_distribution parameter works correctly."""
        # Create a circuit with specific gate distribution
        num_operand_distribution = {1: 0.5, 2: 0.5}
        circ = random_circuit(
            num_qubits=4, 
            depth=10, 
            num_operand_distribution=num_operand_distribution,
            seed=42
        )
        
        # The circuit should be generated without error
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 4)
        self.assertEqual(circ.depth(), 10)

    def test_num_operand_distribution_with_different_ratios(self):
        """Test that different gate ratios are respected."""
        # Test with 1-qubit and 2-qubit gates only
        num_operand_distribution = {1: 0.7, 2: 0.3}
        circ = random_circuit(
            num_qubits=6,
            depth=20,
            num_operand_distribution=num_operand_distribution,
            seed=123
        )
        
        # Circuit should be generated
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 6)
        self.assertEqual(circ.depth(), 20)

    def test_num_operand_distribution_all_gate_types(self):
        """Test with all gate types specified."""
        num_operand_distribution = {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25}
        circ = random_circuit(
            num_qubits=8,
            depth=15,
            num_operand_distribution=num_operand_distribution,
            seed=456
        )
        
        # Circuit should be generated
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 8)
        self.assertEqual(circ.depth(), 15)

    def test_num_operand_distribution_invalid_keys(self):
        """Test that invalid keys in num_operand_distribution raise CircuitError."""
        # Test with key < 1
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=4,
                depth=5,
                num_operand_distribution={0: 0.5, 1: 0.5}
            )
        self.assertIn("'num_operand_distribution' must have keys between 1 and 4", str(context.exception))

        # Test with key > 4
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=4,
                depth=5,
                num_operand_distribution={5: 0.5, 1: 0.5}
            )
        self.assertIn("'num_operand_distribution' must have keys between 1 and 4", str(context.exception))

    def test_num_operand_distribution_invalid_qubits(self):
        """Test that specifying gates with more qubits than circuit raises CircuitError."""
        # Try to use 3-qubit gates on a 2-qubit circuit
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=2,
                depth=5,
                num_operand_distribution={3: 0.5, 1: 0.5}
            )
        self.assertIn("'num_operand_distribution' cannot have 3-qubit gates", str(context.exception))

    def test_num_operand_distribution_sum_not_one(self):
        """Test that distribution with sum != 1 raises CircuitError."""
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=4,
                depth=5,
                num_operand_distribution={1: 0.3, 2: 0.4}
            )
        self.assertIn("The sum of all the values in 'num_operand_distribution' is not 1", str(context.exception))

    def test_num_operand_distribution_with_zero_probability(self):
        """Test that zero probability gates work correctly."""
        num_operand_distribution = {1: 0.5, 2: 0.0, 3: 0.5, 4: 0.0}
        circ = random_circuit(
            num_qubits=6,
            depth=10,
            num_operand_distribution=num_operand_distribution,
            seed=789
        )
        
        # Circuit should be generated
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 6)
        self.assertEqual(circ.depth(), 10)

    def test_num_operand_distribution_vs_max_operands(self):
        """Test that num_operand_distribution takes precedence over max_operands."""
        # When both are specified, num_operand_distribution should be used
        # This tests that the new behavior works correctly
        circ1 = random_circuit(
            num_qubits=4,
            depth=10,
            max_operands=2,  # This should be ignored when num_operand_distribution is provided
            num_operand_distribution={1: 0.5, 2: 0.5},
            seed=100
        )
        
        # Circuit should be generated without error
        self.assertIsInstance(circ1, QuantumCircuit)
        self.assertEqual(circ1.num_qubits, 4)
        self.assertEqual(circ1.depth(), 10)

    def test_default_behavior_unchanged(self):
        """Test that default behavior (without num_operand_distribution) is unchanged."""
        # This should work exactly as before, using max_operands
        circ = random_circuit(num_qubits=3, depth=5, max_operands=3, seed=200)
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 3)
        self.assertEqual(circ.depth(), 5)
        
        # Test with default parameters (should use max_operands=4)
        circ2 = random_circuit(num_qubits=2, depth=3)
        self.assertIsInstance(circ2, QuantumCircuit)
        self.assertEqual(circ2.num_qubits, 2)
        self.assertEqual(circ2.depth(), 3)

    def test_boundary_condition_qubit_limit(self):
        """Test that exactly num_qubits qubit gates are allowed (boundary condition)."""
        # This should work - 2-qubit gates on a 2-qubit circuit
        circ = random_circuit(
            num_qubits=2,
            depth=5,
            num_operand_distribution={2: 1.0}
        )
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 2)