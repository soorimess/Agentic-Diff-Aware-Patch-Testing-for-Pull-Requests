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


if __name__ == "__main__":
    unittest.main()