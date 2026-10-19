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
from test import QiskitTestCase


class TestRandomCircuitNumOperandDistribution(QiskitTestCase):
    """Testing the num_operand_distribution parameter in random_circuit."""

    def test_num_operand_distribution_basic(self):
        """Test that num_operand_distribution parameter works correctly."""
        # Test with a simple distribution
        circ = random_circuit(
            num_qubits=4, 
            depth=10, 
            num_operand_distribution={1: 0.5, 2: 0.5}
        )
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 4)
        self.assertEqual(circ.depth(), 10)

    def test_num_operand_distribution_with_different_ratios(self):
        """Test with different gate ratios."""
        # Test with 1-qubit and 2-qubit gates only
        circ = random_circuit(
            num_qubits=6, 
            depth=20, 
            num_operand_distribution={1: 0.3, 2: 0.7}
        )
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 6)
        self.assertEqual(circ.depth(), 20)

    def test_num_operand_distribution_all_gates(self):
        """Test with all gate types specified."""
        circ = random_circuit(
            num_qubits=5, 
            depth=15, 
            num_operand_distribution={1: 0.2, 2: 0.3, 3: 0.3, 4: 0.2}
        )
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 5)
        self.assertEqual(circ.depth(), 15)

    def test_num_operand_distribution_invalid_keys(self):
        """Test that invalid keys in num_operand_distribution raise CircuitError."""
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=4, 
                depth=10, 
                num_operand_distribution={0: 0.5, 1: 0.5}
            )
        self.assertIn("'num_operand_distribution' must have keys between 1 and 4", str(context.exception))

        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=4, 
                depth=10, 
                num_operand_distribution={5: 0.5, 1: 0.5}
            )
        self.assertIn("'num_operand_distribution' must have keys between 1 and 4", str(context.exception))

    def test_num_operand_distribution_invalid_qubits(self):
        """Test that num_operand_distribution with gates exceeding qubit count raises CircuitError."""
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=3, 
                depth=10, 
                num_operand_distribution={1: 0.2, 4: 0.8}
            )
        self.assertIn("'num_operand_distribution' cannot have 4-qubit gates for circuit with 3 qubits", str(context.exception))

    def test_num_operand_distribution_sum_not_one(self):
        """Test that num_operand_distribution with sum != 1 raises CircuitError."""
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=4, 
                depth=10, 
                num_operand_distribution={1: 0.3, 2: 0.6}
            )
        self.assertIn("The sum of all the values in 'num_operand_distribution' is not 1", str(context.exception))

    def test_num_operand_distribution_with_seed(self):
        """Test that num_operand_distribution works with seed parameter."""
        circ1 = random_circuit(
            num_qubits=4, 
            depth=10, 
            num_operand_distribution={1: 0.5, 2: 0.5},
            seed=42
        )
        circ2 = random_circuit(
            num_qubits=4, 
            depth=10, 
            num_operand_distribution={1: 0.5, 2: 0.5},
            seed=42
        )
        # Should generate identical circuits with same seed
        self.assertEqual(circ1, circ2)

    def test_num_operand_distribution_vs_max_operands(self):
        """Test that num_operand_distribution takes precedence over max_operands."""
        # When both are specified, num_operand_distribution should be used
        circ = random_circuit(
            num_qubits=4, 
            depth=10, 
            max_operands=2,
            num_operand_distribution={1: 0.5, 2: 0.5}
        )
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 4)
        self.assertEqual(circ.depth(), 10)

    def test_num_operand_distribution_empty_dict(self):
        """Test that empty num_operand_distribution works."""
        circ = random_circuit(
            num_qubits=4, 
            depth=10, 
            num_operand_distribution={}
        )
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 4)
        self.assertEqual(circ.depth(), 10)

    def test_num_operand_distribution_zero_probabilities(self):
        """Test that zero probabilities in distribution work."""
        circ = random_circuit(
            num_qubits=4, 
            depth=10, 
            num_operand_distribution={1: 0.0, 2: 1.0}
        )
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 4)
        self.assertEqual(circ.depth(), 10)

    def test_num_operand_distribution_order_independence(self):
        """Test that order of keys in num_operand_distribution doesn't matter."""
        circ1 = random_circuit(
            num_qubits=4, 
            depth=10, 
            num_operand_distribution={3: 0.5, 1: 0.5}
        )
        circ2 = random_circuit(
            num_qubits=4, 
            depth=10, 
            num_operand_distribution={1: 0.5, 3: 0.5}
        )
        self.assertIsInstance(circ1, QuantumCircuit)
        self.assertIsInstance(circ2, QuantumCircuit)
        self.assertEqual(circ1.num_qubits, 4)
        self.assertEqual(circ2.num_qubits, 4)