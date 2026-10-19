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

"""Regression tests for PR #14132: Replace internal representation in ObservablesArray with SparseObservable"""

import numpy as np
import qiskit.quantum_info as qi
from qiskit.primitives.containers.observables_array import ObservablesArray
from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestObservablesArraySparseObservableIntegration(QiskitTestCase):
    """Test cases for the new SparseObservable-based implementation"""

    def test_coerce_observable_returns_sparse_observable(self):
        """Test that coerce_observable now returns SparseObservable instead of dict"""
        # Before the change, this would return a dict
        # After the change, this should return a SparseObservable
        obs = ObservablesArray.coerce_observable("IXYZ")
        
        # Check that it's now a SparseObservable (not a dict)
        self.assertTrue(hasattr(obs, 'num_qubits'))
        self.assertTrue(hasattr(obs, 'coeffs'))
        self.assertTrue(hasattr(obs, 'bit_terms'))

    def test_sparse_observable_conversion_from_sparse_pauli_op(self):
        """Test conversion from SparsePauliOp to SparseObservable"""
        sop = qi.SparsePauliOp("IXYZ")
        obs = ObservablesArray.coerce_observable(sop)
        
        # Should be a SparseObservable
        self.assertTrue(hasattr(obs, 'num_qubits'))
        self.assertTrue(hasattr(obs, 'coeffs'))
        
        # Should have the same number of qubits
        self.assertEqual(obs.num_qubits, 4)
        
        # Should have real coefficients
        self.assertTrue(np.all(np.isreal(obs.coeffs)))

    def test_sparse_observable_conversion_from_pauli(self):
        """Test conversion from Pauli to SparseObservable"""
        pauli = qi.Pauli("IXYZ")
        obs = ObservablesArray.coerce_observable(pauli)
        
        # Should be a SparseObservable
        self.assertTrue(hasattr(obs, 'num_qubits'))
        self.assertTrue(hasattr(obs, 'coeffs'))
        
        # Should have the same number of qubits
        self.assertEqual(obs.num_qubits, 4)

    def test_sparse_observable_conversion_from_string(self):
        """Test conversion from string to SparseObservable"""
        obs = ObservablesArray.coerce_observable("IXYZ")
        
        # Should be a SparseObservable
        self.assertTrue(hasattr(obs, 'num_qubits'))
        self.assertTrue(hasattr(obs, 'coeffs'))
        
        # Should have the correct number of qubits
        self.assertEqual(obs.num_qubits, 4)

    def test_sparse_observable_conversion_from_mapping(self):
        """Test conversion from mapping to SparseObservable"""
        obs_dict = {"IXYZ": 2.0, "ZZZZ": 1.5}
        obs = ObservablesArray.coerce_observable(obs_dict)
        
        # Should be a SparseObservable
        self.assertTrue(hasattr(obs, 'num_qubits'))
        self.assertTrue(hasattr(obs, 'coeffs'))
        
        # Should have the correct number of qubits
        self.assertEqual(obs.num_qubits, 4)

    def test_obs_to_dict_method(self):
        """Test the _obs_to_dict method that converts SparseObservable to dict"""
        # Create a SparseObservable manually
        sop = qi.SparsePauliOp("IXYZ")
        sparse_obs = ObservablesArray.coerce_observable(sop)
        
        # Convert back to dict using the new method
        result_dict = ObservablesArray._obs_to_dict(sparse_obs)
        
        # Should be a dict with correct structure
        self.assertIsInstance(result_dict, dict)
        self.assertIn("IXYZ", result_dict)
        self.assertEqual(result_dict["IXYZ"], 1.0)  # Default coefficient

    def test_array_conversion_behavior(self):
        """Test that __array__ method now returns dict dtype arrays"""
        obs_array = ObservablesArray([{"IXYZ": 1.0}, {"ZZZZ": 2.0}])
        
        # Convert to numpy array
        np_array = np.array(obs_array)
        
        # Should be a numpy array with dtype=object containing dicts
        self.assertIsInstance(np_array, np.ndarray)
        self.assertEqual(np_array.dtype, object)
        
        # Each element should be a dict
        self.assertIsInstance(np_array[0], dict)
        self.assertIsInstance(np_array[1], dict)

    def test_getitem_behavior(self):
        """Test that __getitem__ now returns dict for scalar access"""
        obs_array = ObservablesArray([{"IXYZ": 1.0}, {"ZZZZ": 2.0}])
        
        # Scalar access should return dict
        result = obs_array[0]
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {"IXYZ": 1.0})
        
        # Slice access should return ObservablesArray
        sliced = obs_array[0:1]
        self.assertIsInstance(sliced, ObservablesArray)

    def test_allowed_basis_removal(self):
        """Test that ALLOWED_BASIS class attribute no longer exists"""
        # This should raise AttributeError now
        with self.assertRaises(AttributeError):
            _ = ObservablesArray.ALLOWED_BASIS

    def test_non_hermitian_detection(self):
        """Test that non-Hermitian observables are properly detected"""
        # Create a SparsePauliOp with complex coefficients (non-Hermitian)
        sop = qi.SparsePauliOp("IXYZ", coeffs=[1+1j])
        
        with self.assertRaises(ValueError):
            ObservablesArray.coerce_observable(sop)
            
    def test_repr_behavior(self):
        """Test that __repr__ works with the new implementation"""
        obs_array = ObservablesArray([{"IXYZ": 1.0}, {"ZZZZ": 2.0}])
        repr_str = repr(obs_array)
        self.assertIsInstance(repr_str, str)
        self.assertTrue("ObservablesArray" in repr_str)
        
    def test_tolist_behavior(self):
        """Test that tolist() works with the new implementation"""
        obs_array = ObservablesArray([{"IXYZ": 1.0}, {"ZZZZ": 2.0}])
        result = obs_array.tolist()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], dict)
        self.assertIsInstance(result[1], dict)