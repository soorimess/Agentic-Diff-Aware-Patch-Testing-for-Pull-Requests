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

from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestCircuitRandomFromGraph(QiskitTestCase):
    """Testing qiskit.circuit.random.utils.random_circuit_from_graph"""

    def test_function_exists(self):
        """Test that the function exists and can be imported."""
        # This test should fail before the PR and pass after
        from qiskit.circuit.random.utils import random_circuit_from_graph
        self.assertTrue(callable(random_circuit_from_graph))

    def test_function_has_correct_signature(self):
        """Test that the function has the expected signature."""
        # This test should fail before the PR and pass after
        from qiskit.circuit.random.utils import random_circuit_from_graph
        import inspect
        
        sig = inspect.signature(random_circuit_from_graph)
        # Check key parameters that should be present
        expected_params = [
            'interaction_graph', 'min_2q_gate_per_edge', 'max_operands', 
            'measure', 'conditional', 'reset', 'seed', 'insert_1q_oper',
            'prob_conditional', 'prob_reset'
        ]
        
        for param in expected_params:
            self.assertIn(param, sig.parameters)