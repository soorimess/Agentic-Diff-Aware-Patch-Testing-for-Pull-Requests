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

"""Test for symengine version compatibility workaround in QPY."""

import io
import unittest

from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.qpy import dump, load


class TestSymengineVersionCompatibility(unittest.TestCase):
    """Test cases for symengine version compatibility workaround."""

    def test_parameter_expression_serialization_integration(self):
        """Test ParameterExpression serialization integration with symengine."""
        # Create a circuit with ParameterExpression that would trigger symengine serialization
        param = Parameter('x')
        circuit = QuantumCircuit(2)
        circuit.rx(param, 0)
        circuit.cx(0, 1)
        
        # This test validates that the integration works correctly
        # The PR changes how ParameterExpressions are loaded to handle version mismatches
        qpy_buffer = io.BytesIO()
        dump(circuit, qpy_buffer, use_symengine=True)
        qpy_buffer.seek(0)
        
        # Load the circuit - this exercises the new code path that handles version compatibility
        loaded_circuit = load(qpy_buffer)[0]
        
        # Verify the loaded circuit matches the original
        self.assertEqual(circuit, loaded_circuit)

    def test_parameter_expression_math_operations_integration(self):
        """Test ParameterExpression with mathematical operations integration."""
        # Create a circuit with mathematical ParameterExpression
        param = Parameter('angle')
        complex_expr = param * 2 + 3.14159
        circuit = QuantumCircuit(1)
        circuit.rz(complex_expr, 0)
        
        # Test with symengine serialization
        qpy_buffer = io.BytesIO()
        dump(circuit, qpy_buffer, use_symengine=True)
        qpy_buffer.seek(0)
        
        loaded_circuit = load(qpy_buffer)[0]
        
        # Verify the loaded circuit matches the original
        self.assertEqual(circuit, loaded_circuit)

    def test_multiple_parameter_expressions_integration(self):
        """Test multiple ParameterExpressions integration in one circuit."""
        # Create a circuit with multiple parameters
        param1 = Parameter('theta')
        param2 = Parameter('phi')
        circuit = QuantumCircuit(2)
        circuit.rz(param1, 0)
        circuit.ry(param2, 1)
        circuit.cx(0, 1)
        
        # Test with symengine serialization
        qpy_buffer = io.BytesIO()
        dump(circuit, qpy_buffer, use_symengine=True)
        qpy_buffer.seek(0)
        
        loaded_circuit = load(qpy_buffer)[0]
        
        # Verify the loaded circuit matches the original
        self.assertEqual(circuit, loaded_circuit)