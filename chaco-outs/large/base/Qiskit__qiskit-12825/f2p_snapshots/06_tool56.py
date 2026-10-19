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

"""Test for ContextAwareDynamicalDecoupling pass."""

import unittest

from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import ALAPScheduleAnalysis
from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestContextAwareDynamicalDecoupling(QiskitTestCase):
    """Test the ContextAwareDynamicalDecoupling pass."""

    def test_import_exists(self):
        """Test that ContextAwareDynamicalDecoupling can be imported."""
        # This should work after the PR is applied
        from qiskit.transpiler.passes import ContextAwareDynamicalDecoupling
        # If we get here without ImportError, the import works
        self.assertTrue(True)

    def test_class_instantiation(self):
        """Test that ContextAwareDynamicalDecoupling can be instantiated."""
        # Import the pass - this should work after the PR is applied
        from qiskit.transpiler.passes import ContextAwareDynamicalDecoupling
        
        # Create a minimal mock target
        class MockTarget:
            def __init__(self):
                self.dt = 1.0
                self.pulse_alignment = 1
                self._durations = {"x": 160, "delay": 1000}
                self._coupling_map = None
                
            def durations(self):
                return self._durations
                
            def build_coupling_map(self):
                from qiskit.transpiler.coupling import CouplingMap
                return CouplingMap.from_line(2)
            
            def __getitem__(self, key):
                return {}
                
            def items(self):
                return []
        
        target = MockTarget()
        
        # This should not raise an exception
        dd_pass = ContextAwareDynamicalDecoupling(target=target)
        self.assertIsInstance(dd_pass, ContextAwareDynamicalDecoupling)
        
    def test_parameter_validation(self):
        """Test that the pass validates its parameters correctly."""
        # Import the pass - this should work after the PR is applied
        from qiskit.transpiler.passes import ContextAwareDynamicalDecoupling
        
        # Create a mock target
        class MockTarget:
            def __init__(self):
                self.dt = 1.0
                self.pulse_alignment = 1
                self._durations = {"x": 160, "delay": 1000}
                self._coupling_map = None
                
            def durations(self):
                return self._durations
                
            def build_coupling_map(self):
                from qiskit.transpiler.coupling import CouplingMap
                return CouplingMap.from_line(2)
            
            def __getitem__(self, key):
                return {}
                
            def items(self):
                return []
        
        target = MockTarget()
        
        # Test valid skip_dd_threshold
        dd_pass = ContextAwareDynamicalDecoupling(target=target, skip_dd_threshold=0.9)
        self.assertEqual(dd_pass._skip_dd_threshold, 0.9)
        
        # Test invalid skip_dd_threshold (should raise ValueError)
        with self.assertRaises(ValueError):
            ContextAwareDynamicalDecoupling(target=target, skip_dd_threshold=1.5)
            
        with self.assertRaises(ValueError):
            ContextAwareDynamicalDecoupling(target=target, skip_dd_threshold=-0.1)
            
    def test_get_orthogonal_sequence(self):
        """Test that get_orthogonal_sequence method works."""
        # Import the pass - this should work after the PR is applied
        from qiskit.transpiler.passes import ContextAwareDynamicalDecoupling
        
        # Create a minimal mock target
        class MockTarget:
            def __init__(self):
                self.dt = 1.0
                self.pulse_alignment = 1
                self._durations = {"x": 160, "delay": 1000}
                self._coupling_map = None
                
            def durations(self):
                return self._durations
                
            def build_coupling_map(self):
                from qiskit.transpiler.coupling import CouplingMap
                return CouplingMap.from_line(2)
            
            def __getitem__(self, key):
                return {}
                
            def items(self):
                return []
        
        target = MockTarget()
        
        # Test that we can instantiate and call get_orthogonal_sequence
        dd_pass = ContextAwareDynamicalDecoupling(target=target)
        
        # Test that the method exists and can be called
        spacing, gates = dd_pass.get_orthogonal_sequence(0)
        self.assertIsInstance(spacing, list)
        self.assertIsInstance(gates, list)
        self.assertTrue(len(spacing) > 0)
        self.assertTrue(len(gates) > 0)


if __name__ == "__main__":
    unittest.main()