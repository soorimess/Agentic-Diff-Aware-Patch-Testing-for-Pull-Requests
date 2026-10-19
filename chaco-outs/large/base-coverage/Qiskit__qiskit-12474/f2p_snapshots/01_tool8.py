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

"""Test for the new random_circuit_from_graph function."""

import numpy as np
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.exceptions import CircuitError
from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestRandomCircuitFromGraph(QiskitTestCase):
    """Testing qiskit.circuit.random.random_circuit_from_graph"""

    def test_function_exists(self):
        """Test that the function exists and is importable."""
        try:
            from qiskit.circuit.random.utils import random_circuit_from_graph
            self.assertTrue(callable(random_circuit_from_graph))
        except ImportError:
            self.fail("random_circuit_from_graph should be importable from qiskit.circuit.random.utils")

    def test_basic_functionality_with_graph(self):
        """Test basic functionality with a simple interaction graph."""
        try:
            from qiskit.circuit.random.utils import random_circuit_from_graph
            import rustworkx as rx
            
            # Create a simple interaction graph
            pydi_graph = rx.PyDiGraph()
            pydi_graph.add_nodes_from(range(3))
            pydi_graph.add_edges_from([(0, 1, 0.5), (1, 2, 0.5)])
            
            # Generate circuit
            qc = random_circuit_from_graph(pydi_graph, min_2q_gate_per_edge=1, seed=42)
            
            # Basic checks
            self.assertIsInstance(qc, QuantumCircuit)
            self.assertEqual(qc.num_qubits, 3)
            self.assertGreaterEqual(qc.size(), 1)
        except ImportError:
            self.skipTest("rustworkx not available")

    def test_function_with_list_input(self):
        """Test the function with list input instead of graph object."""
        try:
            from qiskit.circuit.random.utils import random_circuit_from_graph
            
            # Create interaction graph as list
            interaction_graph = [(0, 1, 0.5), (1, 2, 0.5)]
            
            # Generate circuit
            qc = random_circuit_from_graph(interaction_graph, min_2q_gate_per_edge=1, seed=42)
            
            # Basic checks
            self.assertIsInstance(qc, QuantumCircuit)
            self.assertEqual(qc.num_qubits, 3)
            self.assertGreaterEqual(qc.size(), 1)
        except ImportError:
            self.skipTest("rustworkx not available")

    def test_edge_cases_with_no_edges(self):
        """Test edge cases when interaction graph has no edges."""
        try:
            from qiskit.circuit.random.utils import random_circuit_from_graph
            
            # Create a graph with no edges
            import rustworkx as rx
            pydi_graph = rx.PyDiGraph()
            pydi_graph.add_nodes_from(range(3))
            
            # This should work with insert_1q_oper=True (default)
            qc = random_circuit_from_graph(pydi_graph, min_2q_gate_per_edge=1, seed=42)
            self.assertIsInstance(qc, QuantumCircuit)
            self.assertEqual(qc.num_qubits, 3)
            
            # This should raise an error with insert_1q_oper=False
            with self.assertRaises(CircuitError):
                random_circuit_from_graph(pydi_graph, min_2q_gate_per_edge=1, 
                                        insert_1q_oper=False, seed=42)
        except ImportError:
            self.skipTest("rustworkx not available")

    def test_invalid_max_operands(self):
        """Test that invalid max_operands raises CircuitError."""
        try:
            from qiskit.circuit.random.utils import random_circuit_from_graph
            
            import rustworkx as rx
            pydi_graph = rx.PyDiGraph()
            pydi_graph.add_nodes_from(range(3))
            pydi_graph.add_edges_from([(0, 1, 0.5)])
            
            # Test invalid max_operands
            with self.assertRaises(CircuitError):
                random_circuit_from_graph(pydi_graph, max_operands=3, seed=42)
                
            with self.assertRaises(CircuitError):
                random_circuit_from_graph(pydi_graph, max_operands=0, seed=42)
        except ImportError:
            self.skipTest("rustworkx not available")

    def test_invalid_interaction_graph(self):
        """Test that invalid interaction graph raises CircuitError."""
        try:
            from qiskit.circuit.random.utils import random_circuit_from_graph
            
            # Test with invalid graph type
            with self.assertRaises(CircuitError):
                random_circuit_from_graph("invalid_graph", seed=42)
        except ImportError:
            self.skipTest("rustworkx not available")