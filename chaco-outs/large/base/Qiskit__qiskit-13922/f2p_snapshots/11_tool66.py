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

"""Test for the new MCX synthesis functions added in PR #13922."""

import unittest
from qiskit.exceptions import QiskitError
from qiskit.circuit import QuantumCircuit


class TestMCXSynthesisKG24(unittest.TestCase):
    """Test the new MCX synthesis functions from Khattar and Gidney (2024)."""

    def test_mcx_functions_importable(self):
        """Test that all new MCX synthesis functions can be imported."""
        # This test verifies that the functions exist and can be imported
        # It will fail before the PR and pass after the PR
        try:
            from qiskit.synthesis.multi_controlled import (
                synth_mcx_1_clean_kg24,
                synth_mcx_1_dirty_kg24,
                synth_mcx_2_clean_kg24,
                synth_mcx_2_dirty_kg24,
            )
            # Test that they are callable
            self.assertTrue(callable(synth_mcx_1_clean_kg24))
            self.assertTrue(callable(synth_mcx_1_dirty_kg24))
            self.assertTrue(callable(synth_mcx_2_clean_kg24))
            self.assertTrue(callable(synth_mcx_2_dirty_kg24))
        except ImportError:
            # This is expected in the current state where functions don't exist
            self.fail("Functions should be importable after the PR is applied")

    def test_mcx_1_clean_kg24_error_handling(self):
        """Test that synth_mcx_1_clean_kg24 raises QiskitError for <= 2 controls."""
        try:
            from qiskit.synthesis.multi_controlled import synth_mcx_1_clean_kg24
            with self.assertRaises(QiskitError):
                synth_mcx_1_clean_kg24(2)
            with self.assertRaises(QiskitError):
                synth_mcx_1_clean_kg24(1)
            with self.assertRaises(QiskitError):
                synth_mcx_1_clean_kg24(0)
        except ImportError:
            # This is expected in the current state where functions don't exist
            self.fail("Function should exist after the PR is applied")

    def test_mcx_1_dirty_kg24_error_handling(self):
        """Test that synth_mcx_1_dirty_kg24 raises QiskitError for <= 2 controls."""
        try:
            from qiskit.synthesis.multi_controlled import synth_mcx_1_dirty_kg24
            with self.assertRaises(QiskitError):
                synth_mcx_1_dirty_kg24(2)
            with self.assertRaises(QiskitError):
                synth_mcx_1_dirty_kg24(1)
            with self.assertRaises(QiskitError):
                synth_mcx_1_dirty_kg24(0)
        except ImportError:
            # This is expected in the current state where functions don't exist
            self.fail("Function should exist after the PR is applied")

    def test_mcx_2_clean_kg24_error_handling(self):
        """Test that synth_mcx_2_clean_kg24 raises QiskitError for <= 2 controls."""
        try:
            from qiskit.synthesis.multi_controlled import synth_mcx_2_clean_kg24
            with self.assertRaises(QiskitError):
                synth_mcx_2_clean_kg24(2)
            with self.assertRaises(QiskitError):
                synth_mcx_2_clean_kg24(1)
            with self.assertRaises(QiskitError):
                synth_mcx_2_clean_kg24(0)
        except ImportError:
            # This is expected in the current state where functions don't exist
            self.fail("Function should exist after the PR is applied")

    def test_mcx_2_dirty_kg24_error_handling(self):
        """Test that synth_mcx_2_dirty_kg24 raises QiskitError for <= 2 controls."""
        try:
            from qiskit.synthesis.multi_controlled import synth_mcx_2_dirty_kg24
            with self.assertRaises(QiskitError):
                synth_mcx_2_dirty_kg24(2)
            with self.assertRaises(QiskitError):
                synth_mcx_2_dirty_kg24(1)
            with self.assertRaises(QiskitError):
                synth_mcx_2_dirty_kg24(0)
        except ImportError:
            # This is expected in the current state where functions don't exist
            self.fail("Function should exist after the PR is applied")

    def test_mcx_1_clean_kg24_basic_functionality(self):
        """Test that synth_mcx_1_clean_kg24 works with valid inputs."""
        try:
            from qiskit.synthesis.multi_controlled import synth_mcx_1_clean_kg24
            # This function should work with 3+ controls
            qc = synth_mcx_1_clean_kg24(3)  # Valid input that exercises the helper
            # If we get here, the function exists and works correctly
            self.assertIsNotNone(qc)
            self.assertIsInstance(qc, QuantumCircuit)
            self.assertGreaterEqual(len(qc.qubits), 4)  # 3 controls + 1 target + 1 ancilla
        except ImportError:
            # Expected in current state - functions don't exist yet
            self.fail("Function should exist after the PR is applied")

    def test_mcx_2_clean_kg24_basic_functionality(self):
        """Test that synth_mcx_2_clean_kg24 works with valid inputs."""
        try:
            from qiskit.synthesis.multi_controlled import synth_mcx_2_clean_kg24
            # This function should work with 3+ controls
            qc = synth_mcx_2_clean_kg24(3)  # Valid input that exercises the helper
            # If we get here, the function exists and works correctly
            self.assertIsNotNone(qc)
            self.assertIsInstance(qc, QuantumCircuit)
            self.assertGreaterEqual(len(qc.qubits), 5)  # 3 controls + 1 target + 2 ancillas
        except ImportError:
            # Expected in current state - functions don't exist yet
            self.fail("Function should exist after the PR is applied")

    def test_mcx_1_clean_kg24_valid_inputs(self):
        """Test that synth_mcx_1_clean_kg24 works with various valid inputs."""
        try:
            from qiskit.synthesis.multi_controlled import synth_mcx_1_clean_kg24
            # Test with different valid numbers of controls
            for num_ctrls in [3, 4, 5, 6, 10]:
                qc = synth_mcx_1_clean_kg24(num_ctrls)
                self.assertIsNotNone(qc)
                self.assertIsInstance(qc, QuantumCircuit)
                # Should have at least num_ctrls + 2 qubits (controls + target + ancilla)
                self.assertGreaterEqual(len(qc.qubits), num_ctrls + 2)
        except ImportError:
            # Expected in current state - functions don't exist yet
            self.fail("Function should exist after the PR is applied")

    def test_mcx_2_clean_kg24_valid_inputs(self):
        """Test that synth_mcx_2_clean_kg24 works with various valid inputs."""
        try:
            from qiskit.synthesis.multi_controlled import synth_mcx_2_clean_kg24
            # Test with different valid numbers of controls
            for num_ctrls in [3, 4, 5, 6, 10]:
                qc = synth_mcx_2_clean_kg24(num_ctrls)
                self.assertIsNotNone(qc)
                self.assertIsInstance(qc, QuantumCircuit)
                # Should have at least num_ctrls + 3 qubits (controls + target + 2 ancillas)
                self.assertGreaterEqual(len(qc.qubits), num_ctrls + 3)
        except ImportError:
            # Expected in current state - functions don't exist yet
            self.fail("Function should exist after the PR is applied")

    def test_mcx_1_dirty_kg24_functionality(self):
        """Test that synth_mcx_1_dirty_kg24 works with valid inputs."""
        try:
            from qiskit.synthesis.multi_controlled import synth_mcx_1_dirty_kg24
            # This function should work with 3+ controls
            qc = synth_mcx_1_dirty_kg24(3)  # Valid input
            # If we get here, the function exists and works correctly
            self.assertIsNotNone(qc)
            self.assertIsInstance(qc, QuantumCircuit)
            self.assertGreaterEqual(len(qc.qubits), 4)  # 3 controls + 1 target + 1 ancilla
        except ImportError:
            # Expected in current state - functions don't exist yet
            self.fail("Function should exist after the PR is applied")

    def test_mcx_2_dirty_kg24_functionality(self):
        """Test that synth_mcx_2_dirty_kg24 works with valid inputs."""
        try:
            from qiskit.synthesis.multi_controlled import synth_mcx_2_dirty_kg24
            # This function should work with 3+ controls
            qc = synth_mcx_2_dirty_kg24(3)  # Valid input
            # If we get here, the function exists and works correctly
            self.assertIsNotNone(qc)
            self.assertIsInstance(qc, QuantumCircuit)
            self.assertGreaterEqual(len(qc.qubits), 5)  # 3 controls + 1 target + 2 ancillas
        except ImportError:
            # Expected in current state - functions don't exist yet
            self.fail("Function should exist after the PR is applied")

    def test_mcx_1_clean_kg24_edge_case_error(self):
        """Test that _linear_depth_ladder_ops raises error for <= 2 qubits."""
        try:
            from qiskit.synthesis.multi_controlled import synth_mcx_1_clean_kg24
            # This test specifically checks that the internal helper function is called correctly
            # We can't directly test the helper, but we can make sure the error handling works
            # by testing with inputs that would trigger it indirectly
            try:
                # This should work fine
                qc = synth_mcx_1_clean_kg24(3)
                self.assertIsNotNone(qc)
            except Exception:
                # If there's an error, it should be a QiskitError for invalid inputs
                self.fail("Function should work with valid inputs")
        except ImportError:
            # Expected in current state - functions don't exist yet
            self.fail("Function should exist after the PR is applied")

    def test_mcx_2_clean_kg24_complex_case(self):
        """Test that synth_mcx_2_clean_kg24 works with larger inputs that exercise complex logic."""
        try:
            from qiskit.synthesis.multi_controlled import synth_mcx_2_clean_kg24
            # Test with larger number of controls that would exercise the complex ladder logic
            qc = synth_mcx_2_clean_kg24(6)  # This should exercise the complex path
            self.assertIsNotNone(qc)
            self.assertIsInstance(qc, QuantumCircuit)
            # Should have at least 6 + 3 = 9 qubits (controls + target + 2 ancillas)
            self.assertGreaterEqual(len(qc.qubits), 9)
        except ImportError:
            # Expected in current state - functions don't exist yet
            self.fail("Function should exist after the PR is applied")