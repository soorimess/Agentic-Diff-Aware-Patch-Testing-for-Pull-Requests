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
            self.assertTrue(hasattr(qc, 'qubits'))
            self.assertTrue(hasattr(qc, 'data'))
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
            self.assertTrue(hasattr(qc, 'qubits'))
            self.assertTrue(hasattr(qc, 'data'))
        except ImportError:
            # Expected in current state - functions don't exist yet
            self.fail("Function should exist after the PR is applied")