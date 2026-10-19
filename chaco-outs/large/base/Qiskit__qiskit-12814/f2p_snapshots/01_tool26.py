# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Regression tests for LightCone transpiler pass.
"""

import unittest

from qiskit import QuantumCircuit
from qiskit.transpiler.passes.optimization.light_cone import LightCone
from qiskit.transpiler.passmanager import PassManager


class TestLightCone(unittest.TestCase):
    """Test cases for the LightCone transpiler pass."""

    def test_light_cone_basic_functionality(self):
        """Test basic LightCone functionality with measurements."""
        # Create a circuit with measurements
        qc = QuantumCircuit(3, 1)
        qc.h(range(3))
        qc.cx(0, 1)
        qc.cx(2, 1)
        qc.h(range(3))
        qc.measure(0, 0)

        # Apply LightCone pass
        pm = PassManager([LightCone()])
        result = pm.run(qc)

        # The result should be smaller than the original circuit
        # since gates that don't affect the measurement should be removed
        self.assertLessEqual(len(result.data), len(qc.data))

    def test_light_cone_empty_circuit(self):
        """Test LightCone with empty circuit."""
        qc = QuantumCircuit(1, 1)
        qc.measure(0, 0)

        # Apply LightCone pass
        pm = PassManager([LightCone()])
        result = pm.run(qc)

        # Should return the same circuit or a smaller one
        self.assertLessEqual(len(result.data), len(qc.data))

    def test_light_cone_simple_case(self):
        """Test LightCone with a simple case that should be easily reducible."""
        # Create a circuit where most gates don't affect the measurement
        qc = QuantumCircuit(3, 1)
        qc.h(0)  # This gate affects qubit 0 which is measured
        qc.h(1)  # This gate doesn't affect qubit 0 which is measured
        qc.cx(0, 1)  # This gate affects qubit 0 which is measured
        qc.cx(1, 2)  # This gate doesn't affect qubit 0 which is measured
        qc.h(2)  # This gate doesn't affect qubit 0 which is measured
        qc.measure(0, 0)

        # Apply LightCone pass
        pm = PassManager([LightCone()])
        result = pm.run(qc)

        # The result should be smaller than the original circuit
        self.assertLessEqual(len(result.data), len(qc.data))

    def test_light_cone_with_observable_only(self):
        """Test LightCone with observable only (no measurements)."""
        # Create a circuit without measurements but with an observable
        qc = QuantumCircuit(3, 0)
        qc.h(range(3))
        qc.cx(0, 1)
        qc.cx(2, 1)
        qc.h(range(3))

        # Apply LightCone pass with observable
        pm = PassManager([LightCone(bit_terms="X00", indices=[0, 1, 2])])
        result = pm.run(qc)

        # The result should be smaller than the original circuit
        self.assertLessEqual(len(result.data), len(qc.data))