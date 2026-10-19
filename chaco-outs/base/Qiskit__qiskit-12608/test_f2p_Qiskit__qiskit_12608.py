# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=missing-function-docstring, unused-argument

"""Tests for the fix of v2 pulse drawer issue."""

from unittest.mock import Mock
from qiskit import pulse
from qiskit.visualization.pulse_v2 import interface
from test import QiskitTestCase  # pylint: disable=wrong-import-order


class TestV2PulseDrawerFix(QiskitTestCase):
    """Tests for the v2 pulse drawer fix."""

    def test_backend_v2_no_crash(self):
        """Test that BackendV2 objects don't crash the draw function."""
        # Create a mock BackendV2 without configuration/defaults
        backend = Mock()
        backend.name = "test_backend_v2"
        backend.num_qubits = 2
        backend.dt = 1.0e-9
        
        # Remove configuration and defaults to simulate V2 backend
        if hasattr(backend, 'configuration'):
            delattr(backend, 'configuration')
        if hasattr(backend, 'defaults'):
            delattr(backend, 'defaults')
            
        # This should work in the fixed version but crashes in old version
        image = interface.draw(pulse.schedule(), backend=backend)
        self.assertIsNotNone(image)