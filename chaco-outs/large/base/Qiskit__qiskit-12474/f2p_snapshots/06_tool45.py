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

    def test_function_exists_and_is_callable(self):
        """Test that the function exists and is callable."""
        # This test should fail before the PR and pass after
        from qiskit.circuit.random.utils import random_circuit_from_graph
        self.assertTrue(callable(random_circuit_from_graph))

    def test_function_signature_comprehensive(self):
        """Test that the function has the expected signature and defaults."""
        # This test should fail before the PR and pass after
        from qiskit.circuit.random.utils import random_circuit_from_graph
        import inspect
        
        sig = inspect.signature(random_circuit_from_graph)
        
        # Check all expected parameters are present
        expected_params = [
            'interaction_graph', 'min_2q_gate_per_edge', 'max_operands', 
            'measure', 'conditional', 'reset', 'seed', 'insert_1q_oper',
            'prob_conditional', 'prob_reset'
        ]
        
        for param in expected_params:
            self.assertIn(param, sig.parameters)
            
        # Check default values for key parameters
        # These are the defaults that should be set according to the PR
        self.assertEqual(sig.parameters['min_2q_gate_per_edge'].default, 1)
        self.assertEqual(sig.parameters['max_operands'].default, 2)
        self.assertEqual(sig.parameters['measure'].default, False)
        self.assertEqual(sig.parameters['conditional'].default, False)
        self.assertEqual(sig.parameters['reset'].default, False)
        self.assertEqual(sig.parameters['insert_1q_oper'].default, True)
        self.assertEqual(sig.parameters['prob_conditional'].default, 0.1)
        self.assertEqual(sig.parameters['prob_reset'].default, 0.1)
        
        # Check that the function has the right number of parameters
        # (This tests the parameter structure)
        self.assertEqual(len(sig.parameters), 10)