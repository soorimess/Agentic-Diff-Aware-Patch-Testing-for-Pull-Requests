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
import pytest

from qiskit import pulse
from qiskit.providers import BackendV2
from qiskit.visualization.pulse_v2 import device_info, interface
from test import QiskitTestCase


class TestV2BackendPulseDrawer(QiskitTestCase):
    """Tests for V2 backend pulse drawer functionality."""

    def test_v2_backend_without_configuration_defaults_works_after_fix(self):
        """Test that V2 backend without configuration/defaults works correctly after fix."""
        # Create a mock V2 backend that doesn't have configuration/defaults methods
        mock_backend = Mock(spec=BackendV2)
        mock_backend.name = "test_backend"
        mock_backend.dt = 1e-9
        mock_backend.num_qubits = 2
        
        # Mock channel methods that should work for V2 backend
        mock_backend.drive_channel = Mock(return_value=pulse.DriveChannel(0))
        mock_backend.measure_channel = Mock(return_value=pulse.MeasureChannel(0))
        mock_backend.control_channel = Mock(return_value=pulse.ControlChannel(0))
        
        # Create a simple pulse schedule
        schedule = pulse.Schedule()
        schedule.append(pulse.Play(pulse.Constant(100, 0.1), pulse.DriveChannel(0)), inplace=True)
        
        # After the fix, this should not crash with AttributeError
        # Before the fix, this would crash with AttributeError when trying to call .configuration() and .defaults()
        try:
            result = interface.draw(schedule, backend=mock_backend)
            # If we get here, the function didn't crash - that's the main test
            self.assertIsNotNone(result)
        except AttributeError as e:
            # If we get an AttributeError, it means the old code path is still being used
            if "configuration" in str(e) or "defaults" in str(e):
                self.fail("Backend without configuration/defaults should not crash with AttributeError after fix")
            raise

    def test_create_from_backend_v2_backend(self):
        """Test creating backend info from V2 backend works after fix."""
        # Create a mock V2 backend that doesn't have configuration/defaults methods
        mock_backend = Mock(spec=BackendV2)
        mock_backend.name = "test_backend"
        mock_backend.dt = 1e-9
        mock_backend.num_qubits = 2
        
        # Mock channel methods that should work for V2 backend
        mock_backend.drive_channel = Mock(return_value=pulse.DriveChannel(0))
        mock_backend.measure_channel = Mock(return_value=pulse.MeasureChannel(0))
        mock_backend.control_channel = Mock(return_value=pulse.ControlChannel(0))
        
        # After the fix, this should work without raising AttributeError or NotImplementedError
        try:
            backend_info = device_info.OpenPulseBackendInfo.create_from_backend(mock_backend)
            # If we get here without exception, that's good
            self.assertIsNotNone(backend_info)
            # Check that basic properties are set
            self.assertEqual(backend_info.backend_name, "test_backend")
            self.assertEqual(backend_info.dt, 1e-9)
        except AttributeError as e:
            # This would be the old bug - AttributeError about missing configuration/defaults
            if "configuration" in str(e) or "defaults" in str(e):
                self.fail("Backend without configuration/defaults should not crash with AttributeError after fix")
            raise
        except NotImplementedError:
            # This is expected before the fix but should be fixed
            self.fail("Should not raise NotImplementedError after fix")