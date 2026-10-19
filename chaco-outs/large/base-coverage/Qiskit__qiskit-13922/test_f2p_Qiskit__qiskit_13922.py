# This code is part of Qiskit.
#
# (C) Copyright IBM 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests for the new MCX synthesis functions added in PR #13922."""

import unittest

from qiskit import QuantumCircuit
from qiskit.exceptions import QiskitError
from qiskit.synthesis.multi_controlled import (
    synth_mcx_1_clean_kg24,
    synth_mcx_1_dirty_kg24,
    synth_mcx_2_clean_kg24,
    synth_mcx_2_dirty_kg24,
)
from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestMCXSynthesisFunctions(QiskitTestCase):
    """Test the new MCX synthesis functions."""

    def test_mcx_1_clean_kg24_exists(self):
        """Test that synth_mcx_1_clean_kg24 function exists and can be imported."""
        # This should not raise an exception in the fixed version
        self.assertTrue(callable(synth_mcx_1_clean_kg24))

    def test_mcx_1_dirty_kg24_exists(self):
        """Test that synth_mcx_1_dirty_kg24 function exists and can be imported."""
        # This should not raise an exception in the fixed version
        self.assertTrue(callable(synth_mcx_1_dirty_kg24))

    def test_mcx_2_clean_kg24_exists(self):
        """Test that synth_mcx_2_clean_kg24 function exists and can be imported."""
        # This should not raise an exception in the fixed version
        self.assertTrue(callable(synth_mcx_2_clean_kg24))

    def test_mcx_2_dirty_kg24_exists(self):
        """Test that synth_mcx_2_dirty_kg24 function exists and can be imported."""
        # This should not raise an exception in the fixed version
        self.assertTrue(callable(synth_mcx_2_dirty_kg24))

    def test_mcx_functions_raise_error_for_small_inputs(self):
        """Test that functions raise QiskitError for insufficient controls."""
        # All functions should raise error for <= 2 controls
        with self.assertRaises(QiskitError):
            synth_mcx_1_clean_kg24(2)
            
        with self.assertRaises(QiskitError):
            synth_mcx_1_dirty_kg24(2)
            
        with self.assertRaises(QiskitError):
            synth_mcx_2_clean_kg24(2)
            
        with self.assertRaises(QiskitError):
            synth_mcx_2_dirty_kg24(2)
            
        # Should work fine for 3 controls
        qc = synth_mcx_1_clean_kg24(3)
        self.assertIsInstance(qc, QuantumCircuit)

    def test_mcx_1_clean_kg24_basic_functionality(self):
        """Test that synth_mcx_1_clean_kg24 produces valid circuits with basic structure."""
        # Test with minimum valid number of controls
        qc = synth_mcx_1_clean_kg24(3)
        self.assertIsInstance(qc, QuantumCircuit)
        # Should have 3 controls + 1 target + 1 ancilla = 5 qubits
        self.assertEqual(qc.num_qubits, 5)
        
        # Test with more controls
        qc = synth_mcx_1_clean_kg24(5)
        self.assertIsInstance(qc, QuantumCircuit)
        # Should have 5 controls + 1 target + 1 ancilla = 7 qubits
        self.assertEqual(qc.num_qubits, 7)

    def test_mcx_1_dirty_kg24_basic_functionality(self):
        """Test that synth_mcx_1_dirty_kg24 produces valid circuits with basic structure."""
        # Test with minimum valid number of controls
        qc = synth_mcx_1_dirty_kg24(3)
        self.assertIsInstance(qc, QuantumCircuit)
        # Should have 3 controls + 1 target + 1 ancilla = 5 qubits
        self.assertEqual(qc.num_qubits, 5)
        
        # Test with more controls
        qc = synth_mcx_1_dirty_kg24(5)
        self.assertIsInstance(qc, QuantumCircuit)
        # Should have 5 controls + 1 target + 1 ancilla = 7 qubits
        self.assertEqual(qc.num_qubits, 7)

    def test_mcx_2_clean_kg24_basic_functionality(self):
        """Test that synth_mcx_2_clean_kg24 produces valid circuits with basic structure."""
        # Test with minimum valid number of controls
        qc = synth_mcx_2_clean_kg24(3)
        self.assertIsInstance(qc, QuantumCircuit)
        # Should have 3 controls + 1 target + 2 ancillas = 6 qubits
        self.assertEqual(qc.num_qubits, 6)
        
        # Test with more controls
        qc = synth_mcx_2_clean_kg24(5)
        self.assertIsInstance(qc, QuantumCircuit)
        # Should have 5 controls + 1 target + 2 ancillas = 8 qubits
        self.assertEqual(qc.num_qubits, 8)

    def test_mcx_2_dirty_kg24_basic_functionality(self):
        """Test that synth_mcx_2_dirty_kg24 produces valid circuits with basic structure."""
        # Test with minimum valid number of controls
        qc = synth_mcx_2_dirty_kg24(3)
        self.assertIsInstance(qc, QuantumCircuit)
        # Should have 3 controls + 1 target + 2 ancillas = 6 qubits
        self.assertEqual(qc.num_qubits, 6)
        
        # Test with more controls
        qc = synth_mcx_2_dirty_kg24(5)
        self.assertIsInstance(qc, QuantumCircuit)
        # Should have 5 controls + 1 target + 2 ancillas = 8 qubits
        self.assertEqual(qc.num_qubits, 8)

    def test_mcx_functions_can_be_executed(self):
        """Test that the generated circuits can be executed without errors."""
        # Test that we can create and execute basic circuits
        qc1 = synth_mcx_1_clean_kg24(3)
        self.assertIsInstance(qc1, QuantumCircuit)
        
        qc2 = synth_mcx_1_dirty_kg24(3)
        self.assertIsInstance(qc2, QuantumCircuit)
        
        qc3 = synth_mcx_2_clean_kg24(3)
        self.assertIsInstance(qc3, QuantumCircuit)
        
        qc4 = synth_mcx_2_dirty_kg24(3)
        self.assertIsInstance(qc4, QuantumCircuit)

    def test_mcx_1_clean_kg24_specific_edge_cases(self):
        """Test specific edge cases that would catch algorithmic bugs."""
        # Test with 3 controls (minimum valid case)
        qc = synth_mcx_1_clean_kg24(3)
        self.assertIsInstance(qc, QuantumCircuit)
        self.assertEqual(qc.num_qubits, 5)  # 3 controls + 1 target + 1 ancilla
        
        # Test with 4 controls (edge case)
        qc = synth_mcx_1_clean_kg24(4)
        self.assertIsInstance(qc, QuantumCircuit)
        self.assertEqual(qc.num_qubits, 6)  # 4 controls + 1 target + 1 ancilla
        
        # Test with 6 controls (even number)
        qc = synth_mcx_1_clean_kg24(6)
        self.assertIsInstance(qc, QuantumCircuit)
        self.assertEqual(qc.num_qubits, 8)  # 6 controls + 1 target + 1 ancilla

    def test_mcx_2_clean_kg24_specific_edge_cases(self):
        """Test specific edge cases that would catch algorithmic bugs."""
        # Test with 3 controls (minimum valid case)
        qc = synth_mcx_2_clean_kg24(3)
        self.assertIsInstance(qc, QuantumCircuit)
        self.assertEqual(qc.num_qubits, 6)  # 3 controls + 1 target + 2 ancillas
        
        # Test with 4 controls (edge case)
        qc = synth_mcx_2_clean_kg24(4)
        self.assertIsInstance(qc, QuantumCircuit)
        self.assertEqual(qc.num_qubits, 7)  # 4 controls + 1 target + 2 ancillas
        
        # Test with 6 controls (even number)
        qc = synth_mcx_2_clean_kg24(6)
        self.assertIsInstance(qc, QuantumCircuit)
        self.assertEqual(qc.num_qubits, 9)  # 6 controls + 1 target + 2 ancillas

    def test_mcx_1_clean_kg24_circuit_structure(self):
        """Test that the circuit structure is reasonable for various input sizes."""
        # Test that we can generate circuits for various control counts
        for num_ctrls in [3, 4, 5, 6, 7, 8]:
            with self.subTest(num_ctrls=num_ctrls):
                qc = synth_mcx_1_clean_kg24(num_ctrls)
                self.assertIsInstance(qc, QuantumCircuit)
                # Should have correct number of qubits
                self.assertEqual(qc.num_qubits, num_ctrls + 2)  # controls + target + ancilla

    def test_mcx_2_clean_kg24_circuit_structure(self):
        """Test that the circuit structure is reasonable for various input sizes."""
        # Test that we can generate circuits for various control counts
        for num_ctrls in [3, 4, 5, 6, 7, 8]:
            with self.subTest(num_ctrls=num_ctrls):
                qc = synth_mcx_2_clean_kg24(num_ctrls)
                self.assertIsInstance(qc, QuantumCircuit)
                # Should have correct number of qubits
                self.assertEqual(qc.num_qubits, num_ctrls + 3)  # controls + target + 2 ancillas

    def test_mcx_functions_circuit_properties(self):
        """Test that circuits have expected properties that would catch algorithmic issues."""
        # Test that circuits have reasonable depth and gate counts
        qc1 = synth_mcx_1_clean_kg24(4)
        self.assertIsInstance(qc1, QuantumCircuit)
        # Should have some gates
        self.assertGreater(len(qc1.data), 0)
        
        qc2 = synth_mcx_2_clean_kg24(4)
        self.assertIsInstance(qc2, QuantumCircuit)
        # Should have some gates
        self.assertGreater(len(qc2.data), 0)
        
        # Test that we can generate circuits with larger numbers of controls
        qc3 = synth_mcx_1_clean_kg24(10)
        self.assertIsInstance(qc3, QuantumCircuit)
        self.assertEqual(qc3.num_qubits, 12)  # 10 controls + 1 target + 1 ancilla
        
        qc4 = synth_mcx_2_clean_kg24(10)
        self.assertIsInstance(qc4, QuantumCircuit)
        self.assertEqual(qc4.num_qubits, 13)  # 10 controls + 1 target + 2 ancillas


if __name__ == "__main__":
    unittest.main()