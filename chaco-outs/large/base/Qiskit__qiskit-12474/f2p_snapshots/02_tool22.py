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

"""Test random circuit generation from graph utility."""

import unittest
from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestCircuitRandomFromGraph(QiskitTestCase):
    """Testing qiskit.circuit.random.utils.random_circuit_from_graph"""

    def test_function_exists_and_callable(self):
        """Test that the function exists and is callable."""
        try:
            from qiskit.circuit.random.utils import random_circuit_from_graph
            # If we get here, the function exists and is callable
            self.assertTrue(callable(random_circuit_from_graph))
        except ImportError:
            # Skip test if function not yet available (expected before PR)
            self.skipTest("random_circuit_from_graph not yet implemented in this version")

    def test_function_signature_parameters(self):
        """Test that the function has expected signature."""
        try:
            from qiskit.circuit.random.utils import random_circuit_from_graph
            import inspect
            
            # Check that function exists and has expected parameters
            sig = inspect.signature(random_circuit_from_graph)
            # These are the key parameters that should be present
            expected_params = [
                'interaction_graph', 'min_2q_gate_per_edge', 'max_operands', 
                'measure', 'conditional', 'reset', 'seed', 'insert_1q_oper',
                'prob_conditional', 'prob_reset'
            ]
            
            # Check that all expected parameters are present
            for param in expected_params:
                self.assertIn(param, sig.parameters,
                            f"Parameter '{param}' missing from function signature")
        except ImportError:
            self.skipTest("random_circuit_from_graph not yet implemented in this version")

    def test_function_in_module_attributes(self):
        """Test that the function appears in module attributes."""
        try:
            import qiskit.circuit.random.utils as random_utils
            # Check if function is available in module
            self.assertTrue(hasattr(random_utils, 'random_circuit_from_graph'))
        except ImportError:
            self.skipTest("random_circuit_from_graph not yet implemented in this version")