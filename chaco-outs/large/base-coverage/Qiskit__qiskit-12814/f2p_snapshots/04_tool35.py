# This code is part of Qiskit.
#
# (C) Copyright IBM 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test LightCone transpiler pass."""

import unittest

from qiskit import QuantumCircuit
from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestLightCone(QiskitTestCase):
    """Test LightCone pass."""

    def test_light_cone_import_and_basic_functionality(self):
        """Test that LightCone can be imported and basic instantiation works."""
        # This test should fail before the PR is applied and pass after
        try:
            from qiskit.transpiler.passes.optimization.light_cone import LightCone
            
            # Test that we can create instances
            lc1 = LightCone()
            self.assertIsNotNone(lc1)
            
            # Test instantiation with valid parameters
            lc2 = LightCone(bit_terms="X", indices=[0])
            self.assertIsNotNone(lc2)
            
        except ImportError:
            # This is expected before the PR is applied
            self.fail("LightCone should be importable after the PR is applied")

    def test_light_cone_error_handling(self):
        """Test that LightCone raises appropriate errors for invalid inputs."""
        from qiskit.transpiler.passes.optimization.light_cone import LightCone
        
        # Test that providing bit_terms without indices raises ValueError with correct message
        with self.assertRaises(ValueError) as context:
            LightCone(bit_terms="X", indices=None)
        self.assertIn("`indices` must be non-empty when providing `bit_terms`", str(context.exception))
        
        # Test that providing empty indices raises ValueError with correct message
        with self.assertRaises(ValueError) as context:
            LightCone(bit_terms="X", indices=[])
        self.assertIn("`indices` must be non-empty when providing `bit_terms`", str(context.exception))
        
        # Test that invalid characters in bit_terms raises ValueError with correct message
        with self.assertRaises(ValueError) as context:
            LightCone(bit_terms="W", indices=[0])
        self.assertIn("`bit_terms` should contain only characters", str(context.exception))
        
        # Test that mismatched lengths raises ValueError with correct message
        with self.assertRaises(ValueError) as context:
            LightCone(bit_terms="XX", indices=[0])
        self.assertIn("`bit_terms` must be the same length as `indices`", str(context.exception))

    def test_remove_final_measurements_calc_final_ops_exists(self):
        """Test that calc_final_ops function exists in remove_final_measurements module."""
        try:
            from qiskit.transpiler.passes.utils.remove_final_measurements import calc_final_ops
            self.assertTrue(callable(calc_final_ops))
        except ImportError:
            # This is expected before the PR is applied
            self.fail("calc_final_ops should be importable after the PR is applied")


if __name__ == "__main__":
    unittest.main()