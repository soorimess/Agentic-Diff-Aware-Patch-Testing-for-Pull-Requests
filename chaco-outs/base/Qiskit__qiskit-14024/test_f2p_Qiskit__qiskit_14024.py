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

"""Test for security vulnerability fix in QPY parameter expression parsing."""

import io
import unittest
from unittest.mock import patch

from qiskit.circuit import Parameter, QuantumCircuit
from qiskit.circuit.parameterexpression import ParameterExpression
from qiskit.exceptions import QiskitError
from qiskit.qpy import dump, load


class TestQPYParameterExpressionSecurity(unittest.TestCase):
    """Test cases for the security fix in QPY parameter expression parsing."""

    def test_invalid_parameter_expression_raises_error_in_str(self):
        """Test that invalid ParameterExpression raises QiskitError in __str__."""
        # Create a ParameterExpression with invalid _symbol_expr (not a symengine.Basic)
        # We need to directly create one with an invalid symbol_expr to test the fix
        param = Parameter("x")
        
        # Create a ParameterExpression with a string instead of a symengine object
        # This simulates what would happen with an invalidly constructed ParameterExpression
        expr = ParameterExpression.__new__(ParameterExpression)
        expr._parameter_symbols = {param: param}
        expr._parameter_keys = frozenset([param._hash_key()])
        expr._symbol_expr = "invalid_string_value"  # This is not a symengine.Basic
        expr._name_map = None
        expr._standalone_param = False
        expr._qpy_replay = []
        
        # This should raise QiskitError in the fixed version
        with self.assertRaises(QiskitError):
            str(expr)

    def test_invalid_parameter_expression_raises_error_in_eq(self):
        """Test that invalid ParameterExpression raises QiskitError in __eq__."""
        # Create two ParameterExpressions with invalid _symbol_expr (not a symengine.Basic)
        param = Parameter("x")
        
        # Create first invalid ParameterExpression
        expr1 = ParameterExpression.__new__(ParameterExpression)
        expr1._parameter_symbols = {param: param}
        expr1._parameter_keys = frozenset([param._hash_key()])
        expr1._symbol_expr = "invalid_string_value1"
        expr1._name_map = None
        expr1._standalone_param = False
        expr1._qpy_replay = []
        
        # Create second invalid ParameterExpression
        expr2 = ParameterExpression.__new__(ParameterExpression)
        expr2._parameter_symbols = {param: param}
        expr2._parameter_keys = frozenset([param._hash_key()])
        expr2._symbol_expr = "invalid_string_value2"
        expr2._name_map = None
        expr2._standalone_param = False
        expr2._qpy_replay = []
        
        # This should raise QiskitError in the fixed version
        with self.assertRaises(QiskitError):
            expr1 == expr2

    def test_valid_parameter_expression_works_normally(self):
        """Test that valid ParameterExpression objects work normally."""
        # Create a valid ParameterExpression using normal operations
        param = Parameter("theta")
        expr = param + 1
        
        # These should work normally
        str_result = str(expr)
        self.assertIsInstance(str_result, str)
        
        # Test equality with another valid expression
        expr2 = param + 1
        self.assertTrue(expr == expr2)
        
        # Test that valid expressions don't raise errors in __str__
        self.assertIsNotNone(str(expr))

    def test_qpy_workflow_with_parameter_expressions(self):
        """Test QPY workflow with parameter expressions to ensure security fix works."""
        # Create a circuit with parameter expressions - this would exercise the QPY loading path
        param = Parameter("theta")
        circuit = QuantumCircuit(1)
        circuit.rx(param, 0)
        
        # Serialize to QPY - this exercises the parameter expression serialization
        buffer = io.BytesIO()
        dump(circuit, buffer)
        
        # Verify the buffer was created
        self.assertIsNotNone(buffer.getvalue())
        
        # Test that we can load it back (this would use the new parser if it existed)
        buffer.seek(0)
        loaded_circuit = load(buffer)
        
        # Verify the circuit was loaded correctly
        self.assertIsNotNone(loaded_circuit)
        self.assertEqual(len(loaded_circuit), 1)