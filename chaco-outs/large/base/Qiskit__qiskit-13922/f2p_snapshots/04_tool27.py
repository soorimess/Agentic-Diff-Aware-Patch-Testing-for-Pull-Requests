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
from qiskit.synthesis.multi_controlled import (
    synth_mcx_1_clean_kg24,
    synth_mcx_1_dirty_kg24,
    synth_mcx_2_clean_kg24,
    synth_mcx_2_dirty_kg24,
)


class TestMCXSynthesisKG24(unittest.TestCase):
    """Test the new MCX synthesis functions from Khattar and Gidney (2024)."""

    def test_mcx_1_clean_kg24_exists(self):
        """Test that synth_mcx_1_clean_kg24 function exists and can be imported."""
        # This test should fail in the current codebase since the function doesn't exist yet
        self.assertTrue(callable(synth_mcx_1_clean_kg24))

    def test_mcx_1_dirty_kg24_exists(self):
        """Test that synth_mcx_1_dirty_kg24 function exists and can be imported."""
        # This test should fail in the current codebase since the function doesn't exist yet
        self.assertTrue(callable(synth_mcx_1_dirty_kg24))

    def test_mcx_2_clean_kg24_exists(self):
        """Test that synth_mcx_2_clean_kg24 function exists and can be imported."""
        # This test should fail in the current codebase since the function doesn't exist yet
        self.assertTrue(callable(synth_mcx_2_clean_kg24))

    def test_mcx_2_dirty_kg24_exists(self):
        """Test that synth_mcx_2_dirty_kg24 function exists and can be imported."""
        # This test should fail in the current codebase since the function doesn't exist yet
        self.assertTrue(callable(synth_mcx_2_dirty_kg24))

    def test_mcx_1_clean_kg24_raises_error_for_small_inputs(self):
        """Test that synth_mcx_1_clean_kg24 raises QiskitError for <= 2 controls."""
        with self.assertRaises(QiskitError):
            synth_mcx_1_clean_kg24(2)
        with self.assertRaises(QiskitError):
            synth_mcx_1_clean_kg24(1)
        with self.assertRaises(QiskitError):
            synth_mcx_1_clean_kg24(0)

    def test_mcx_1_dirty_kg24_raises_error_for_small_inputs(self):
        """Test that synth_mcx_1_dirty_kg24 raises QiskitError for <= 2 controls."""
        with self.assertRaises(QiskitError):
            synth_mcx_1_dirty_kg24(2)
        with self.assertRaises(QiskitError):
            synth_mcx_1_dirty_kg24(1)
        with self.assertRaises(QiskitError):
            synth_mcx_1_dirty_kg24(0)

    def test_mcx_2_clean_kg24_raises_error_for_small_inputs(self):
        """Test that synth_mcx_2_clean_kg24 raises QiskitError for <= 2 controls."""
        with self.assertRaises(QiskitError):
            synth_mcx_2_clean_kg24(2)
        with self.assertRaises(QiskitError):
            synth_mcx_2_clean_kg24(1)
        with self.assertRaises(QiskitError):
            synth_mcx_2_clean_kg24(0)

    def test_mcx_2_dirty_kg24_raises_error_for_small_inputs(self):
        """Test that synth_mcx_2_dirty_kg24 raises QiskitError for <= 2 controls."""
        with self.assertRaises(QiskitError):
            synth_mcx_2_dirty_kg24(2)
        with self.assertRaises(QiskitError):
            synth_mcx_2_dirty_kg24(1)
        with self.assertRaises(QiskitError):
            synth_mcx_2_dirty_kg24(0)