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

"""Test for regression of ParameterVector behavior change."""

import unittest

from qiskit.circuit import ParameterVector


class TestParameterVectorResize(unittest.TestCase):
    """Test ParameterVector resize behavior."""

    def test_resize_index_returns_correct_position(self):
        """Test that index() returns the correct position after resize."""
        # This tests the specific issue mentioned in #12541
        pv = ParameterVector("theta", 20)
        last = pv[-1]
        pv.resize(3)
        
        # After the fix: index should raise ValueError because the element no longer exists
        # (since old elements are deleted when resizing)
        with self.assertRaises(ValueError):
            pv.index(last)

    def test_resize_params_returns_only_current_elements(self):
        """Test that params property only returns currently existing elements."""
        pv = ParameterVector("theta", 20)
        pv.resize(3)
        
        # After the fix: params should return only 3 elements
        self.assertEqual(len(pv.params), 3)
        self.assertEqual(len(pv), 3)

    def test_resize_len_returns_correct_length(self):
        """Test that len() returns the correct current length."""
        pv = ParameterVector("theta", 20)
        pv.resize(3)
        
        # After the fix: len should return 3 (current actual length)
        self.assertEqual(len(pv), 3)

    def test_resize_iter_only_iterates_current_elements(self):
        """Test that __iter__ only iterates current elements."""
        pv = ParameterVector("theta", 20)
        pv.resize(3)
        
        # After the fix: __iter__ should iterate over only 3 elements
        elements = list(pv)
        self.assertEqual(len(elements), 3)

    def test_resize_str_shows_only_current_elements(self):
        """Test that __str__ only shows current elements."""
        pv = ParameterVector("theta", 20)
        pv.resize(3)
        
        # After the fix: __str__ should show only 3 elements
        str_repr = str(pv)
        # Should contain the string representation with 3 elements
        self.assertIn("[", str_repr)
        self.assertIn("]", str_repr)
        # Count the number of parameters in the string representation
        param_count = str_repr.count("theta[")
        self.assertEqual(param_count, 3)

    def test_resize_getitem_works_correctly(self):
        """Test that __getitem__ works correctly after resize."""
        pv = ParameterVector("theta", 20)
        pv.resize(3)
        
        # Should be able to access elements 0, 1, 2
        self.assertEqual(pv[0].name, "theta[0]")
        self.assertEqual(pv[1].name, "theta[1]")
        self.assertEqual(pv[2].name, "theta[2]")
        
        # Should raise IndexError for out of bounds access (after fix)
        with self.assertRaises(IndexError):
            _ = pv[3]

    def test_resize_shrink_and_expand_preserves_elements(self):
        """Test that shrinking and then expanding preserves element identity."""
        pv = ParameterVector("theta", 20)
        original_element = pv[19]  # Get element that will be removed
        pv.resize(3)  # Shrink to 3 elements
        pv.resize(20)  # Expand back to 20 elements
        
        # The element at index 19 should be the same as the original one
        # (this tests the UUID preservation behavior)
        self.assertEqual(pv[19], original_element)