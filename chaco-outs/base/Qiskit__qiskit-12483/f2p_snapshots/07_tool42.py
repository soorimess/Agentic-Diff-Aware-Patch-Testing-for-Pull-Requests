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

"""Test for the num_operand_distribution parameter in random_circuit."""

import unittest
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.random import random_circuit
from qiskit.circuit.exceptions import CircuitError
from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestRandomCircuitNumOperandDistribution(QiskitTestCase):
    """Testing the num_operand_distribution parameter in random_circuit."""

    def test_num_operand_distribution_parameter_exists(self):
        """Test that the num_operand_distribution parameter can be used."""
        # This should not raise an error in the new version
        try:
            circ = random_circuit(
                num_qubits=4, 
                depth=5, 
                num_operand_distribution={1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25}
            )
            self.assertIsInstance(circ, QuantumCircuit)
        except TypeError as e:
            # If this fails with TypeError, it means the parameter doesn't exist
            if "unexpected keyword argument" in str(e):
                self.fail("num_operand_distribution parameter not found in random_circuit")
            raise

    def test_default_behavior_unchanged(self):
        """Test that default behavior is unchanged when parameter is not provided."""
        # This should work the same as before
        circ = random_circuit(num_qubits=4, depth=5)
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 4)
        self.assertEqual(circ.depth(), 5)

    def test_distribution_validation_keys(self):
        """Test that invalid keys in distribution raise CircuitError."""
        # Test key out of range (less than 1)
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=4, 
                depth=5, 
                num_operand_distribution={0: 0.5, 1: 0.5}
            )
        self.assertIn("'num_operand_distribution' must have keys between 1 and 4", str(context.exception))
        
        # Test key out of range (greater than 4)
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=4, 
                depth=5, 
                num_operand_distribution={5: 0.5, 1: 0.5}
            )
        self.assertIn("'num_operand_distribution' must have keys between 1 and 4", str(context.exception))

    def test_distribution_validation_sum(self):
        """Test that distribution with sum != 1 raises CircuitError."""
        with self.assertRaises(CircuitError) as context:
            random_circuit(
                num_qubits=4, 
                depth=5, 
                num_operand_distribution={1: 0.3, 2: 0.3, 3: 0.3}  # Sum = 0.9
            )
        self.assertIn("The sum of all the values in 'num_operand_distribution' is not 1", str(context.exception))


if __name__ == '__main__':
    unittest.main()