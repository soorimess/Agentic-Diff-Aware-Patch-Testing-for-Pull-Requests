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

"""Tests for the multi-controlled X gate synthesis functions."""

from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestMCXSynthesisFunctions(QiskitTestCase):
    """Test that MCX gates use the new synthesis functions from the synthesis library."""

    def test_mcx_recursive_synthesis_function_exists(self):
        """Test that the new synth_mcx_1_clean_b95 function exists."""
        # This test should fail in the current state (before PR) because the function doesn't exist
        # but should pass after the PR is applied
        from qiskit.synthesis.multi_controlled import synth_mcx_1_clean_b95

    def test_mcx_vchain_dirty_synthesis_function_exists(self):
        """Test that the new synth_mcx_n_dirty_i15 function exists."""
        # This test should fail in the current state (before PR) because the function doesn't exist
        # but should pass after the PR is applied
        from qiskit.synthesis.multi_controlled import synth_mcx_n_dirty_i15

    def test_mcx_vchain_clean_synthesis_function_exists(self):
        """Test that the new synth_mcx_n_clean_m15 function exists."""
        # This test should fail in the current state (before PR) because the function doesn't exist
        # but should pass after the PR is applied
        from qiskit.synthesis.multi_controlled import synth_mcx_n_clean_m15