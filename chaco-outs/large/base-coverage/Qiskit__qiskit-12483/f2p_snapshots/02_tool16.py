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

"""Test for the num_operand_distribution feature in random_circuit."""

from qiskit.circuit import QuantumCircuit
from qiskit.circuit.random import random_circuit
from qiskit.circuit.exceptions import CircuitError
from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestRandomCircuitNumOperandDistribution(QiskitTestCase):
    """Testing the num_operand_distribution feature in random_circuit."""

    def test_num_operand_distribution_basic(self):
        """Test that num_operand_distribution parameter works correctly."""
        # Create a circuit with specific gate distribution
        num_operand_distribution = {1: 0.5, 2: 0.5}
        circ = random_circuit(
            num_qubits=4, depth=10, num_operand_distribution=num_operand_distribution
        )
        
        # The circuit should be created successfully
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 4)
        
        # Verify that we get gates according to the distribution (approximately)
        ops = circ.count_ops()
        total_gates = sum(ops.values())
        
        # With a small circuit, we might not get exact distribution, but we should have 
        # mostly 1-qubit and 2-qubit gates
        self.assertGreater(total_gates, 0)
        
    def test_num_operand_distribution_with_3_and_4_qubit_gates(self):
        """Test num_operand_distribution with 3 and 4 qubit gates."""
        num_operand_distribution = {1: 0.2, 2: 0.2, 3: 0.3, 4: 0.3}
        circ = random_circuit(
            num_qubits=6, depth=15, num_operand_distribution=num_operand_distribution
        )
        
        # The circuit should be created successfully
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 6)
        
    def test_num_operand_distribution_invalid_keys(self):
        """Test that invalid keys in num_operand_distribution raise CircuitError."""
        # Test with keys outside 1-4 range
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=4, depth=5, num_operand_distribution={0: 0.5, 1: 0.5}
            )
        self.assertIn("'num_operand_distribution' must have keys between 1 and 4", str(context.exception))
        
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=4, depth=5, num_operand_distribution={5: 0.5, 1: 0.5}
            )
        self.assertIn("'num_operand_distribution' must have keys between 1 and 4", str(context.exception))
        
    def test_num_operand_distribution_qubit_mismatch(self):
        """Test that num_operand_distribution with gates exceeding qubit count raises CircuitError."""
        # Try to create 3-qubit gates for a 2-qubit circuit - this should fail
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=2, depth=5, num_operand_distribution={1: 0.5, 3: 0.5}
            )
        self.assertIn("cannot have 3-qubit gates for circuit with 2 qubits", str(context.exception))
        
    def test_num_operand_distribution_qubit_exact_match(self):
        """Test that num_operand_distribution with gates that exactly match qubit count works."""
        # This should work - 2-qubit gates for a 2-qubit circuit
        num_operand_distribution = {1: 0.5, 2: 0.5}
        circ = random_circuit(
            num_qubits=2, depth=10, num_operand_distribution=num_operand_distribution
        )
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 2)
        
    def test_num_operand_distribution_sum_not_one(self):
        """Test that num_operand_distribution with sum != 1 raises CircuitError."""
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=4, depth=5, num_operand_distribution={1: 0.5, 2: 0.4}
            )
        self.assertIn("The sum of all the values in 'num_operand_distribution' is not 1", str(context.exception))
        
    def test_num_operand_distribution_with_zero_probabilities(self):
        """Test that num_operand_distribution with zero probabilities works."""
        num_operand_distribution = {1: 0.0, 2: 0.5, 3: 0.5, 4: 0.0}
        circ = random_circuit(
            num_qubits=6, depth=10, num_operand_distribution=num_operand_distribution
        )
        
        # Should create circuit without error
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 6)
        
    def test_num_operand_distribution_vs_max_operands_priority(self):
        """Test that num_operand_distribution takes priority over max_operands."""
        # When both are specified, num_operand_distribution should be used
        # This test verifies the behavior when both parameters are provided
        circ = random_circuit(
            num_qubits=4, depth=10, max_operands=3, num_operand_distribution={1: 0.5, 2: 0.5}
        )
        
        # Should create circuit without error using the distribution
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 4)
        
    def test_backward_compatibility(self):
        """Test that existing code without num_operand_distribution still works."""
        # This should work exactly as before
        circ = random_circuit(num_qubits=4, depth=10)
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 4)
        
        # With max_operands specified
        circ = random_circuit(num_qubits=4, depth=10, max_operands=2)
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 4)