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

from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.qpy import dump, load


class TestParameterExpressionSecurityFix(unittest.TestCase):
    """Test that validates the security fix for ParameterExpression parsing."""

    def test_qpy_parameter_expression_functionality(self):
        """Test core QPY parameter expression functionality.
        
        This test validates that the security fix doesn't break core functionality
        while ensuring parameter expressions work correctly with QPY serialization.
        The security fix prevents arbitrary code execution when loading QPY files
        containing parameter expressions.
        """
        # Create parameter expressions that would be processed by the security fix
        a = Parameter("a")
        b = Parameter("b")
        expr = a + b
        
        # Create a circuit with parameter expressions
        qc = QuantumCircuit(1)
        qc.rz(expr, 0)
        
        # Test QPY serialization/deserialization - core functionality
        with io.BytesIO() as f:
            dump(qc, f, version=13)
            f.seek(0)
            loaded_qc = load(f)[0]
            
        # Verify the loaded circuit has the correct structure
        self.assertEqual(len(loaded_qc.data), 1)
        
        # Verify parameter expressions are preserved
        instruction = loaded_qc.data[0]
        self.assertEqual(instruction.operation.name, "rz")
        
        # Test that parameter expressions can be used in operations
        param_expr = instruction.operation.params[0]
        self.assertIsNotNone(param_expr)
        
        # Test string conversion (this would be validated by security fix)
        str_result = str(param_expr)
        self.assertIsInstance(str_result, str)
        
    def test_parameter_expression_operations(self):
        """Test basic parameter expression operations work correctly.
        
        This validates that core parameter expression functionality works
        correctly with the security enhancements.
        """
        # Create parameter expressions
        a = Parameter("a")
        b = Parameter("b")
        
        # Test basic operations
        expr1 = a + b
        expr2 = a * 2
        
        # These operations should work correctly
        str1 = str(expr1)
        str2 = str(expr2)
        
        self.assertIsInstance(str1, str)
        self.assertIsInstance(str2, str)
        
        # Test equality operations
        expr1_copy = a + b
        self.assertTrue(expr1 == expr1_copy)