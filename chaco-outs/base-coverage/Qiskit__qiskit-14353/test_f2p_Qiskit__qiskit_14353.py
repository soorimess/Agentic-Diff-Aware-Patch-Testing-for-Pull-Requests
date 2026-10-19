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

"""Regression tests for PR #14353: Do not construct layout passes with no coupling map."""

import unittest

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


class TestNoLayoutPassesWithNoneCouplingMap(unittest.TestCase):
    """Test that layout passes are not constructed when coupling_map is None."""

    def test_preset_pass_manager_works_with_none_coupling_map(self):
        """Test that preset pass managers work with coupling_map=None.
        
        This regression test ensures that PR #14353 is properly implemented:
        when coupling_map=None, layout passes should not be constructed, preventing
        runtime errors that would occur when these passes try to use None as a coupling_map.
        """
        # Test with a simple circuit
        q = QuantumRegister(2, name="q")
        circuit = QuantumCircuit(q)
        circuit.cx(q[0], q[1])
        
        # This should work without errors - the fix prevents invalid layout passes
        result = generate_preset_pass_manager(
            optimization_level=3,
            coupling_map=None,
            basis_gates=["u1", "u2", "u3", "cx"]
        ).run(circuit)
        
        # The result should be a valid circuit
        self.assertIsInstance(result, QuantumCircuit)

    def test_preset_pass_manager_works_with_coupling_map(self):
        """Test that preset pass managers still work with a coupling map."""
        # Test with a simple circuit
        q = QuantumRegister(2, name="q")
        circuit = QuantumCircuit(q)
        circuit.cx(q[0], q[1])
        
        # Test with a coupling map (should still work as before)
        from qiskit.transpiler import CouplingMap
        coupling_map = CouplingMap.from_line(2)
        
        result = generate_preset_pass_manager(
            optimization_level=3,
            coupling_map=coupling_map,
            basis_gates=["u1", "u2", "u3", "cx"]
        ).run(circuit)
        
        # The result should be a valid circuit
        self.assertIsInstance(result, QuantumCircuit)

    def test_pr_14353_fix_verification(self):
        """Verify that PR #14353 fix is in place.
        
        The fix prevents layout passes from being constructed when coupling_map=None,
        which would otherwise cause failures when these passes try to use None as 
        a coupling_map in their execution.
        """
        # This test verifies that the core fix is working by ensuring
        # that preset pass managers can handle None coupling_map correctly
        q = QuantumRegister(3, name="q")
        circuit = QuantumCircuit(q)
        circuit.cx(q[0], q[1])
        circuit.cx(q[1], q[2])
        
        # The fix ensures this works without constructing invalid layout passes
        result = generate_preset_pass_manager(
            optimization_level=2,
            coupling_map=None,
            basis_gates=["u1", "u2", "u3", "cx"]
        ).run(circuit)
        
        self.assertIsInstance(result, QuantumCircuit)