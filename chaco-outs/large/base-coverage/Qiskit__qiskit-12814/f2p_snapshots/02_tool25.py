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

    def test_light_cone_class_exists_and_instantiable(self):
        """Test that LightCone class exists and can be instantiated."""
        # This test should fail before the PR is applied and pass after
        from qiskit.transpiler.passes.optimization.light_cone import LightCone
        
        # Test basic instantiation
        lc = LightCone()
        self.assertIsNotNone(lc)
        
        # Test instantiation with valid parameters
        lc2 = LightCone(bit_terms="X", indices=[0])
        self.assertIsNotNone(lc2)
        
        # Test instantiation with None parameters (should work)
        lc3 = LightCone(bit_terms=None, indices=None)
        self.assertIsNotNone(lc3)

    def test_light_cone_error_handling(self):
        """Test that LightCone raises appropriate errors for invalid inputs."""
        from qiskit.transpiler.passes.optimization.light_cone import LightCone
        
        # Test that providing bit_terms without indices raises ValueError
        with self.assertRaises(ValueError):
            LightCone(bit_terms="X", indices=None)
            
        # Test that providing empty indices raises ValueError
        with self.assertRaises(ValueError):
            LightCone(bit_terms="X", indices=[])

    def test_remove_final_measurements_calc_final_ops_exists(self):
        """Test that calc_final_ops function exists in remove_final_measurements module."""
        from qiskit.transpiler.passes.utils.remove_final_measurements import calc_final_ops
        self.assertTrue(callable(calc_final_ops))


if __name__ == "__main__":
    unittest.main()