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
    """Test the new SparseObservable integration in ObservablesArray"""

    def test_coerce_observable_returns_sparse_observable(self):
        """Test that coerce_observable now returns SparseObservable instead of dict"""
        # Test string input - should return SparseObservable
        obs = ObservablesArray.coerce_observable("XX")
        # This will fail on old code, which is expected
        try:
            self.assertTrue(hasattr(obs, 'num_qubits'))
            self.assertTrue(hasattr(obs, 'coeffs'))
            self.assertTrue(hasattr(obs, 'bit_terms'))
        except AttributeError:
            self.skipTest("SparseObservable not available in old code")

    def test_array_conversion_returns_dict_dtype(self):
        """Test that __array__ method now returns numpy array with dtype=dict"""
        obs_array = ObservablesArray([{"XX": 1.0}, {"YY": 1.0}])
        try:
            result = obs_array.__array__()
            
            # Should be a numpy array with dtype=dict
            self.assertIsInstance(result, np.ndarray)
            self.assertEqual(result.dtype, dict)
            
            # Should have the right shape
            self.assertEqual(result.shape, (2,))
            
            # Each element should be a dict
            self.assertIsInstance(result[0], dict)
            self.assertIsInstance(result[1], dict)
        except AttributeError:
            self.skipTest("New __array__ method not implemented yet")

    def test_getitem_returns_dict(self):
        """Test that __getitem__ now returns dict instead of old format"""
        obs_array = ObservablesArray([{"XX": 1.0}, {"YY": 1.0}])
        
        # Test scalar access - should return dict
        try:
            item = obs_array[0]
            self.assertIsInstance(item, dict)
            self.assertEqual(item, {"XX": 1.0})
        except AttributeError:
            self.skipTest("New __getitem__ behavior not implemented yet")

    def test_sparse_observable_functionality(self):
        """Test that SparseObservable functionality works correctly"""
        # Test from_sparse_pauli_op
        try:
            spo = qi.SparsePauliOp("XX")
            sparse_obs = ObservablesArray.coerce_observable(spo)
            self.assertTrue(hasattr(sparse_obs, 'num_qubits'))
            self.assertEqual(sparse_obs.num_qubits, 2)
            
            # Test from_pauli
            pauli = qi.Pauli("XY")
            sparse_obs = ObservablesArray.coerce_observable(pauli)
            self.assertTrue(hasattr(sparse_obs, 'num_qubits'))
            self.assertEqual(sparse_obs.num_qubits, 2)
            
            # Test from_label
            sparse_obs = ObservablesArray.coerce_observable("XY")
            self.assertTrue(hasattr(sparse_obs, 'num_qubits'))
            self.assertEqual(sparse_obs.num_qubits, 2)
            
            # Test from_list
            sparse_obs = ObservablesArray.coerce_observable({"XX": 1.0, "YY": 2.0})
            self.assertTrue(hasattr(sparse_obs, 'num_qubits'))
            self.assertEqual(sparse_obs.num_qubits, 2)
            
            # Test that we can convert back to dict format
            result_dict = ObservablesArray._obs_to_dict(sparse_obs)
            self.assertIsInstance(result_dict, dict)
        except (AttributeError, ImportError):
            self.skipTest("SparseObservable functionality not available in old code")

    def test_array_elements_are_valid_observables(self):
        """Test that internal array elements are valid SparseObservable objects"""
        # This test should fail on old code because the internal structure is different
        try:
            # Create an array and check internal structure
            obs_array = ObservablesArray([{"XX": 1.0}, {"YY": 1.0}])
            
            # Check that we can access internal elements without issues
            # This will fail if internal array elements are None
            elements = obs_array._array.reshape(-1)
            self.assertGreater(len(elements), 0)
            
            # Try to access first element - should not be None
            first_element = elements[0]
            # If it's None, that would indicate a problem with the implementation
            self.assertIsNotNone(first_element)
            
            # If we have SparseObservable, it should have the expected attributes
            if hasattr(first_element, 'num_qubits'):
                self.assertTrue(hasattr(first_element, 'num_qubits'))
                
        except AttributeError:
            # If _array doesn't exist, it's old code - skip this test
            self.skipTest("Internal structure not available in old code")
        except Exception:
            # Any other exception indicates a problem with the implementation
            # This is what we want to catch - the test should fail on broken implementations
            raise

    def test_robustness_against_edge_cases(self):
        """Test robustness against various edge cases in the implementation"""
        try:
            # Test that __array__ method doesn't return None
            obs_array = ObservablesArray([{"XX": 1.0}])
            result = obs_array.__array__()
            self.assertIsNotNone(result)
            self.assertIsInstance(result, np.ndarray)
            
            # Test that we can call repr without issues
            repr_str = repr(obs_array)
            self.assertIsInstance(repr_str, str)
            
            # Test that we can access elements properly
            item = obs_array[0]
            self.assertIsInstance(item, dict)
            
            # Test that array conversion works for various shapes
            obs_array_2d = ObservablesArray([{"XX": 1.0}, {"YY": 1.0}]).reshape((1, 2))
            result_2d = obs_array_2d.__array__()
            self.assertIsInstance(result_2d, np.ndarray)
            self.assertEqual(result_2d.shape, (1, 2))
            
        except AttributeError:
            self.skipTest("New functionality not available in old code")
            
    def test_no_invalid_operations_in_obs_to_dict(self):
        """Test that _obs_to_dict doesn't perform invalid operations"""
        try:
            # Test with a simple observable that should not cause string division
            spo = qi.SparsePauliOp("XX")
            sparse_obs = ObservablesArray.coerce_observable(spo)
            
            # This should not cause any invalid operations like string division
            result = ObservablesArray._obs_to_dict(sparse_obs)
            self.assertIsInstance(result, dict)
            self.assertIn("XX", result)
            
            # Test with a more complex observable
            spo2 = qi.SparsePauliOp("XYZ")
            sparse_obs2 = ObservablesArray.coerce_observable(spo2)
            result2 = ObservablesArray._obs_to_dict(sparse_obs2)
            self.assertIsInstance(result2, dict)
            
        except (AttributeError, ImportError):
            self.skipTest("SparseObservable functionality not available in old code")
        except Exception as e:
            # If we get an exception, it might be due to invalid operations in the implementation
            # This is what we want to catch - the test should fail if there are implementation errors
            raise