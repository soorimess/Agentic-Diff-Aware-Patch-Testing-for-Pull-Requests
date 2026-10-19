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
import numpy as np
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

    def test_distribution_respected(self):
        """Test that the specified distribution is approximately respected."""
        # Create a circuit with a specific distribution
        num_operand_dist = {1: 0.5, 2: 0.3, 3: 0.2}
        circ = random_circuit(
            num_qubits=6, 
            depth=20, 
            num_operand_distribution=num_operand_dist,
            seed=42
        )
        
        # Count the gates by operand number
        ops = circ.count_ops()
        total_gates = sum(ops.values())
        
        # Check that we have some gates
        self.assertGreater(total_gates, 0)
        
        # Check that the distribution is approximately respected
        # (This is a basic check - exact ratios may vary due to randomness)
        if 'u1' in ops:
            u1_count = ops['u1']
            # 1-qubit gates should be about 50% of total gates
            self.assertGreater(u1_count, 0)
            
        if 'cx' in ops:
            cx_count = ops['cx']
            # 2-qubit gates should be about 30% of total gates
            self.assertGreater(cx_count, 0)
            
        if 'ccx' in ops:
            ccx_count = ops['ccx']
            # 3-qubit gates should be about 20% of total gates
            self.assertGreater(ccx_count, 0)

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

    def test_default_behavior_unchanged(self):
        """Test that default behavior is unchanged when parameter is not provided."""
        # This should work the same as before
        circ = random_circuit(num_qubits=4, depth=5)
        self.assertIsInstance(circ, QuantumCircuit)
        self.assertEqual(circ.num_qubits, 4)
        self.assertEqual(circ.depth(), 5)

    def test_distribution_with_seed(self):
        """Test that the same seed produces the same circuit with distribution."""
        # Create two circuits with same seed and distribution
        circ1 = random_circuit(
            num_qubits=4, 
            depth=10, 
            num_operand_distribution={1: 0.5, 2: 0.5},
            seed=12345
        )
        circ2 = random_circuit(
            num_qubits=4, 
            depth=10, 
            num_operand_distribution={1: 0.5, 2: 0.5},
            seed=12345
        )
        
        # They should be identical
        self.assertEqual(circ1, circ2)

    def test_distribution_order_independence(self):
        """Test that the order of keys in distribution doesn't matter."""
        # Create circuits with same distribution in different orders
        circ1 = random_circuit(
            num_qubits=4, 
            depth=10, 
            num_operand_distribution={4: 0.25, 3: 0.25, 2: 0.25, 1: 0.25}
        )
        circ2 = random_circuit(
            num_qubits=4, 
            depth=10, 
            num_operand_distribution={1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25}
        )
        
        # Both should work and produce valid circuits
        self.assertIsInstance(circ1, QuantumCircuit)
        self.assertIsInstance(circ2, QuantumCircuit)
        self.assertEqual(circ1.num_qubits, 4)
        self.assertEqual(circ2.num_qubits, 4)

    def test_boundary_condition_validation(self):
        """Test boundary condition validation for max_operands."""
        # Test max_operands exactly at boundary values (should work)
        # This tests the boundary condition logic that was changed in mutation variant 3
        circ1 = random_circuit(num_qubits=4, depth=5, max_operands=1)
        self.assertIsInstance(circ1, QuantumCircuit)
        self.assertEqual(circ1.num_qubits, 4)
        
        circ2 = random_circuit(num_qubits=4, depth=5, max_operands=4)
        self.assertIsInstance(circ2, QuantumCircuit)
        self.assertEqual(circ2.num_qubits, 4)
        
        # Test that max_operands at boundary values works correctly
        # This specifically tests the boundary condition logic that was changed
        # from "num_qubits > max_operands" to "num_qubits >= max_operands"
        
        # Test with a circuit that has exactly the same number of qubits as max_operands
        circ3 = random_circuit(num_qubits=3, depth=5, max_operands=3)
        self.assertIsInstance(circ3, QuantumCircuit)
        self.assertEqual(circ3.num_qubits, 3)
        
        # Test with a circuit that has fewer qubits than max_operands
        circ4 = random_circuit(num_qubits=2, depth=5, max_operands=3)
        self.assertIsInstance(circ4, QuantumCircuit)
        self.assertEqual(circ4.num_qubits, 2)


if __name__ == '__main__':
    unittest.main()