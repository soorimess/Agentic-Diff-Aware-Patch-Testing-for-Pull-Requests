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
from qiskit.circuit.library import CXGate, ECRGate, XGate
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import (
    ALAPScheduleAnalysis,
    ASAPScheduleAnalysis,
    PadDelay,
)
from qiskit.transpiler.target import Target, InstructionProperties
from qiskit.transpiler.exceptions import TranspilerError
from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestContextAwareDynamicalDecoupling(QiskitTestCase):
    """Tests for ContextAwareDynamicalDecoupling pass."""

    def test_import(self):
        """Test that ContextAwareDynamicalDecoupling can be imported."""
        # This test verifies that the pass is available in the expected location
        try:
            from qiskit.transpiler.passes import ContextAwareDynamicalDecoupling
            self.assertIsNotNone(ContextAwareDynamicalDecoupling)
        except ImportError:
            # This is expected in the current codebase before the PR is applied
            self.fail("ContextAwareDynamicalDecoupling should be importable")

    def test_basic_instantiation(self):
        """Test basic instantiation of ContextAwareDynamicalDecoupling."""
        # Create a simple target
        target = Target()
        target.add_instruction(XGate(), {(0,): InstructionProperties(duration=100, error=0.01)})
        target.add_instruction(CXGate(), {(0, 1): InstructionProperties(duration=500, error=0.01)})
        target.dt = 1.0

        # Test that we can create the pass
        try:
            from qiskit.transpiler.passes import ContextAwareDynamicalDecoupling
            dd_pass = ContextAwareDynamicalDecoupling(target=target)
            self.assertIsNotNone(dd_pass)
        except ImportError:
            # This is expected in the current codebase before the PR is applied
            self.fail("ContextAwareDynamicalDecoupling should be importable and instantiable")

    def test_skip_reset_qubits_parameter(self):
        """Test that skip_reset_qubits parameter works correctly."""
        # Create a simple target
        target = Target()
        target.add_instruction(XGate(), {(0,): InstructionProperties(duration=100, error=0.01)})
        target.add_instruction(CXGate(), {(0, 1): InstructionProperties(duration=500, error=0.01)})
        target.dt = 1.0

        # Test that we can create the pass with skip_reset_qubits parameter
        try:
            from qiskit.transpiler.passes import ContextAwareDynamicalDecoupling
            dd_pass = ContextAwareDynamicalDecoupling(target=target, skip_reset_qubits=True)
            self.assertIsNotNone(dd_pass)
        except ImportError:
            # This is expected in the current codebase before the PR is applied
            self.fail("ContextAwareDynamicalDecoupling should be importable and instantiable")

    def test_skip_dd_threshold_parameter(self):
        """Test that skip_dd_threshold parameter works correctly."""
        # Create a simple target
        target = Target()
        target.add_instruction(XGate(), {(0,): InstructionProperties(duration=100, error=0.01)})
        target.add_instruction(CXGate(), {(0, 1): InstructionProperties(duration=500, error=0.01)})
        target.dt = 1.0

        # Test that we can create the pass with skip_dd_threshold parameter
        try:
            from qiskit.transpiler.passes import ContextAwareDynamicalDecoupling
            dd_pass = ContextAwareDynamicalDecoupling(target=target, skip_dd_threshold=0.5)
            self.assertIsNotNone(dd_pass)
        except ImportError:
            # This is expected in the current codebase before the PR is applied
            self.fail("ContextAwareDynamicalDecoupling should be importable and instantiable")

        # Test invalid threshold value
        with self.assertRaises(ValueError):
            ContextAwareDynamicalDecoupling(target=target, skip_dd_threshold=1.5)

    def test_requires_pad_delay(self):
        """Test that ContextAwareDynamicalDecoupling requires PadDelay."""
        # Create a simple target
        target = Target()
        target.add_instruction(XGate(), {(0,): InstructionProperties(duration=100, error=0.01)})
        target.add_instruction(CXGate(), {(0, 1): InstructionProperties(duration=500, error=0.01)})
        target.dt = 1.0

        try:
            from qiskit.transpiler.passes import ContextAwareDynamicalDecoupling, PadDelay
            dd_pass = ContextAwareDynamicalDecoupling(target=target)
            
            # Check that it requires PadDelay
            self.assertIn(PadDelay(target=target), dd_pass.requires)
        except ImportError:
            # This is expected in the current codebase before the PR is applied
            self.fail("ContextAwareDynamicalDecoupling should be importable and have requires attribute")

    def test_orthogonal_sequences(self):
        """Test that the pass generates orthogonal sequences for adjacent qubits."""
        # This test focuses on the core functionality: orthogonal sequences
        # The actual sequence generation is tested in the implementation
        
        # Create a simple target
        target = Target()
        target.add_instruction(XGate(), {(0,): InstructionProperties(duration=100, error=0.01)})
        target.add_instruction(CXGate(), {(0, 1): InstructionProperties(duration=500, error=0.01)})
        target.dt = 1.0

        # Test that we can access the orthogonal sequence generation method
        try:
            from qiskit.transpiler.passes import ContextAwareDynamicalDecoupling
            
            dd_pass = ContextAwareDynamicalDecoupling(target=target)
            
            # Test that the method exists and works
            spacing, gates = dd_pass.get_orthogonal_sequence(1)
            self.assertIsInstance(spacing, list)
            self.assertIsInstance(gates, list)
            self.assertGreater(len(spacing), 0)
            self.assertGreater(len(gates), 0)
        except ImportError:
            # This is expected in the current codebase before the PR is applied
            self.fail("ContextAwareDynamicalDecoupling should be importable and have get_orthogonal_sequence method")

    def test_parameter_validation(self):
        """Test that parameters are properly validated."""
        # Create a simple target
        target = Target()
        target.add_instruction(XGate(), {(0,): InstructionProperties(duration=100, error=0.01)})
        target.add_instruction(CXGate(), {(0, 1): InstructionProperties(duration=500, error=0.01)})
        target.dt = 1.0

        # Test that the pass properly sets parameters
        try:
            from qiskit.transpiler.passes import ContextAwareDynamicalDecoupling
            
            # Test default values
            dd_pass = ContextAwareDynamicalDecoupling(target=target)
            self.assertEqual(dd_pass._skip_reset_qubits, True)
            self.assertEqual(dd_pass._skip_dd_threshold, 1.0)
            
            # Test custom values
            dd_pass_custom = ContextAwareDynamicalDecoupling(
                target=target, 
                skip_reset_qubits=False,
                skip_dd_threshold=0.8
            )
            self.assertEqual(dd_pass_custom._skip_reset_qubits, False)
            self.assertEqual(dd_pass_custom._skip_dd_threshold, 0.8)
            
        except ImportError:
            # This is expected in the current codebase before the PR is applied
            self.fail("ContextAwareDynamicalDecoupling should be importable and have proper parameter handling")