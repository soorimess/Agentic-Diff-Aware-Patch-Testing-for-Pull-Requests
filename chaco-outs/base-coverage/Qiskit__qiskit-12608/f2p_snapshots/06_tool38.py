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

from collections import defaultdict
from unittest.mock import Mock

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

    def test_create_from_backend_v2_backend_properties(self):
        """Test creating backend info from V2 backend works after fix with key properties."""
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
            # Check that basic properties are set correctly
            self.assertEqual(backend_info.backend_name, "test_backend")
            self.assertEqual(backend_info.dt, 1e-9)
            
            # Check that the channel frequency map is initialized properly (not None)
            self.assertIsNotNone(backend_info._chan_freq_map)
            # For V2 backends, we expect empty channel frequency map since no frequencies are available
            # This is the key behavior: it should not crash trying to populate frequencies
            self.assertEqual(len(backend_info._chan_freq_map), 0)
            
            # Check that the qubit channel map is initialized properly (not None)
            self.assertIsNotNone(backend_info._qubit_channel_map)
            
            # Should have entries for qubits 0 and 1
            self.assertIn(0, backend_info._qubit_channel_map)
            self.assertIn(1, backend_info._qubit_channel_map)
            
            # Check that the qubit channel map has the expected channels
            qubit_0_channels = backend_info._qubit_channel_map[0]
            self.assertIn(pulse.DriveChannel(0), qubit_0_channels)
            self.assertIn(pulse.MeasureChannel(0), qubit_0_channels)
            
            # Verify that the backend has no configuration method (this is key to the V2 path)
            self.assertFalse(hasattr(mock_backend, 'configuration'))
            self.assertFalse(hasattr(mock_backend, 'defaults'))
            
        except AttributeError as e:
            # This would be the old bug - AttributeError about missing configuration/defaults
            if "configuration" in str(e) or "defaults" in str(e):
                self.fail("Backend without configuration/defaults should not crash with AttributeError after fix")
            raise
        except NotImplementedError:
            # This is expected before the fix but should be fixed
            self.fail("Should not raise NotImplementedError after fix")
            
    def test_v2_backend_path_is_taken_not_configuration_path(self):
        """Test that V2 backend correctly takes the V2 path, not the configuration path."""
        # Create a mock V2 backend that doesn't have configuration/defaults methods
        mock_backend = Mock(spec=BackendV2)
        mock_backend.name = "test_backend"
        mock_backend.dt = 1e-9
        mock_backend.num_qubits = 2
        
        # Mock channel methods that should work for V2 backend
        mock_backend.drive_channel = Mock(return_value=pulse.DriveChannel(0))
        mock_backend.measure_channel = Mock(return_value=pulse.MeasureChannel(0))
        mock_backend.control_channel = Mock(return_value=pulse.ControlChannel(0))
        
        # Test that the backend doesn't have configuration/defaults (this is what triggers V2 path)
        # If it had these methods, it would take the old path and we'd get AttributeError when calling them
        self.assertFalse(hasattr(mock_backend, 'configuration'))
        self.assertFalse(hasattr(mock_backend, 'defaults'))
        
        # The key test: this should work without trying to call configuration/defaults
        try:
            backend_info = device_info.OpenPulseBackendInfo.create_from_backend(mock_backend)
            # If we get here, the V2 path was taken correctly
            self.assertIsNotNone(backend_info)
            # Verify the backend name and dt are correctly set from V2 backend
            self.assertEqual(backend_info.backend_name, "test_backend")
            self.assertEqual(backend_info.dt, 1e-9)
        except AttributeError as e:
            # If we get AttributeError about missing configuration/defaults, 
            # it means the old path was taken instead of V2 path
            if "configuration" in str(e) or "defaults" in str(e):
                self.fail("V2 backend should take V2 path, not configuration path")
            raise

    def test_backend_with_both_configuration_and_defaults_still_works(self):
        """Test that backends with both configuration and defaults still work (old path)."""
        # Create a mock backend that has configuration and defaults (old-style)
        mock_backend = Mock()
        mock_backend.name = "test_backend"
        mock_backend.dt = 1e-9
        mock_backend.num_qubits = 2
        
        # Mock configuration and defaults methods (old-style backend)
        mock_config = Mock()
        mock_config.backend_name = "test_backend"
        mock_config.dt = 1e-9
        mock_config.n_qubits = 2
        mock_config.u_channel_lo = []
        mock_config.drive = Mock(return_value=pulse.DriveChannel(0))
        mock_config.measure = Mock(return_value=pulse.MeasureChannel(0))
        mock_config.control = Mock(return_value=[pulse.ControlChannel(0)])
        
        mock_defaults = Mock()
        mock_defaults.qubit_freq_est = [4.5e9, 4.6e9]
        mock_defaults.meas_freq_est = [6.5e9, 6.6e9]
        
        mock_backend.configuration = Mock(return_value=mock_config)
        mock_backend.defaults = Mock(return_value=mock_defaults)
        
        # This should work with the old path
        try:
            backend_info = device_info.OpenPulseBackendInfo.create_from_backend(mock_backend)
            # If we get here, the old path works correctly
            self.assertIsNotNone(backend_info)
            self.assertEqual(backend_info.backend_name, "test_backend")
            self.assertEqual(backend_info.dt, 1e-9)
        except Exception as e:
            # If it fails, it's likely because the condition logic is wrong
            # The test should pass if the fix is correct
            self.fail(f"Old-style backend should work but failed: {e}")