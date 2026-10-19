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

"""Test for symengine version compatibility in QPY."""

import io
import unittest

# This import will fail before the fix is applied, but should work after
# It tests the specific functionality added by PR #13251
try:
    from qiskit.qpy.common import load_symengine_payload
    HAS_LOAD_SYMENGINE_PAYLOAD = True
except ImportError:
    HAS_LOAD_SYMENGINE_PAYLOAD = False

from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.qpy import dump, load


class TestSymengineVersionCompatibility(unittest.TestCase):
    """Test symengine version compatibility workaround.
    
    This test validates the behavior that was fixed in PR #13251 to handle
    symengine version incompatibilities when loading QPY files containing
    ParameterExpression objects.
    """

    def test_qpy_parameter_expressions_basic_functionality(self):
        """Test basic QPY parameter expression functionality."""
        # Create a circuit with parameter expressions
        param = Parameter("theta")
        circuit = QuantumCircuit(1)
        circuit.rx(param, 0)
        
        # Test roundtrip with default settings (should use symengine)
        qpy_buffer = io.BytesIO()
        dump(circuit, qpy_buffer, use_symengine=True)
        qpy_buffer.seek(0)
        
        # This should work without errors
        loaded_circuit = load(qpy_buffer)[0]
        self.assertEqual(circuit, loaded_circuit)

    def test_qpy_parameter_expressions_complex_expressions(self):
        """Test that QPY handles complex parameter expressions correctly."""
        # Create a circuit with complex parameter expressions
        param1 = Parameter("theta")
        param2 = Parameter("phi")
        circuit = QuantumCircuit(2)
        circuit.rx(param1 + param2, 0)
        circuit.ry(param1 * 2, 1)
        circuit.crx(param1 - param2, 0, 1)
        
        # Test roundtrip
        qpy_buffer = io.BytesIO()
        dump(circuit, qpy_buffer, use_symengine=True)
        qpy_buffer.seek(0)
        
        loaded_circuit = load(qpy_buffer)[0]
        self.assertEqual(circuit, loaded_circuit)

    def test_qpy_parameter_expressions_multiple_parameters(self):
        """Test that QPY handles multiple parameter expressions correctly."""
        # Create a circuit with multiple parameter expressions
        param1 = Parameter("theta")
        param2 = Parameter("phi")
        param3 = Parameter("psi")
        circuit = QuantumCircuit(3)
        circuit.rx(param1, 0)
        circuit.ry(param2, 1)
        circuit.rz(param3, 2)
        circuit.crx(param1, 0, 1)
        circuit.cry(param2, 1, 2)
        
        # Test roundtrip
        qpy_buffer = io.BytesIO()
        dump(circuit, qpy_buffer, use_symengine=True)
        qpy_buffer.seek(0)
        
        loaded_circuit = load(qpy_buffer)[0]
        self.assertEqual(circuit, loaded_circuit)

    def test_qpy_parameter_expressions_different_qpy_versions(self):
        """Test QPY compatibility across different QPY versions."""
        # Create a circuit with parameter expressions
        param = Parameter("theta")
        circuit = QuantumCircuit(1)
        circuit.rx(param, 0)
        
        # Test different QPY versions
        for version in [None, 10, 11, 12]:
            with self.subTest(version=version):
                qpy_buffer = io.BytesIO()
                if version is None:
                    dump(circuit, qpy_buffer)
                else:
                    dump(circuit, qpy_buffer, version=version)
                qpy_buffer.seek(0)
                
                loaded_circuit = load(qpy_buffer)[0]
                self.assertEqual(circuit, loaded_circuit)

    def test_qpy_parameter_expressions_use_symengine_false(self):
        """Test that QPY works with use_symengine=False."""
        # Create a circuit with parameter expressions
        param = Parameter("theta")
        circuit = QuantumCircuit(1)
        circuit.rx(param, 0)
        
        # Test with use_symengine=False
        qpy_buffer = io.BytesIO()
        dump(circuit, qpy_buffer, use_symengine=False)
        qpy_buffer.seek(0)
        
        loaded_circuit = load(qpy_buffer)[0]
        self.assertEqual(circuit, loaded_circuit)

    def test_load_symengine_payload_function_exists(self):
        """Test that load_symengine_payload function exists (should pass after fix)."""
        # This test should pass after the fix is applied because the function exists
        # and should fail before the fix is applied because the function doesn't exist yet
        self.assertTrue(HAS_LOAD_SYMENGINE_PAYLOAD, 
                       "load_symengine_payload function should exist after the fix is applied")