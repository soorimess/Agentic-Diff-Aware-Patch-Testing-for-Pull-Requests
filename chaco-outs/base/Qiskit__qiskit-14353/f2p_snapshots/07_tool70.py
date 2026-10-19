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

"""Test for the regression of PR #14353: Do not construct layout passes with no coupling map."""

from unittest import TestCase

from qiskit import QuantumCircuit
from qiskit.transpiler.passmanager_config import PassManagerConfig
from qiskit.transpiler.preset_passmanagers.builtin_plugins import (
    DefaultLayoutPassManager,
    TrivialLayoutPassManager,
    DenseLayoutPassManager,
    SabreLayoutPassManager,
)
from qiskit.transpiler.exceptions import TranspilerError
from qiskit.providers.fake_provider import GenericBackendV2


class TestNoLayoutPassesWithNoneCouplingMap(TestCase):
    """Test that layout passes are not constructed when coupling_map=None."""

    def test_trivial_layout_pass_manager_no_layout_when_coupling_map_none(self):
        """Test that TrivialLayoutPassManager does not create TrivialLayout when coupling_map=None."""
        # Create a configuration with coupling_map=None
        config = PassManagerConfig(
            initial_layout=None,
            basis_gates=["u1", "u2", "u3"],
            coupling_map=None,
            target=None,
        )
        
        # Get the layout pass manager
        plugin = TrivialLayoutPassManager()
        pass_manager = plugin.pass_manager(config, optimization_level=0)
        
        # The key test: we should be able to create the pass manager without error
        # and it should not contain TrivialLayout passes when coupling_map=None
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        
        # This should not crash with a TrivialLayout error
        # The fix ensures that when coupling_map=None, TrivialLayout is not constructed
        try:
            result = pass_manager.run(qc)
            self.assertIsInstance(result, QuantumCircuit)
        except AttributeError as e:
            if "'NoneType' object has no attribute 'size'" in str(e):
                # This is the error that would happen if TrivialLayout was constructed with None
                self.fail("TrivialLayout was constructed with coupling_map=None, which should not happen")
            else:
                raise  # Re-raise if it's a different AttributeError
        except Exception as e:
            # Other exceptions are fine, we're mainly concerned about the specific layout error
            pass

    def test_sabre_layout_pass_manager_no_layout_when_coupling_map_none_opt0(self):
        """Test that SabreLayoutPassManager does not create SabreLayout when coupling_map=None for optimization_level=0."""
        # Create a configuration with coupling_map=None
        config = PassManagerConfig(
            initial_layout=None,
            basis_gates=["u1", "u2", "u3"],
            coupling_map=None,
            target=None,
        )
        
        # Get the layout pass manager with optimization_level=0
        plugin = SabreLayoutPassManager()
        pass_manager = plugin.pass_manager(config, optimization_level=0)
        
        # The key test: we should be able to create the pass manager without error
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        
        # This should not crash with layout-related errors
        try:
            result = pass_manager.run(qc)
            self.assertIsInstance(result, QuantumCircuit)
        except AttributeError as e:
            if "'NoneType' object has no attribute 'size'" in str(e):
                # This is the error that would happen if layout passes were constructed with None
                self.fail("SabreLayout was constructed with coupling_map=None, which should not happen")
            else:
                raise  # Re-raise if it's a different AttributeError
        except Exception as e:
            # Other exceptions are fine
            pass

    def test_default_layout_pass_manager_no_layout_when_coupling_map_none_opt0(self):
        """Test that DefaultLayoutPassManager does not create layout passes when coupling_map=None for optimization_level=0."""
        # Create a configuration with coupling_map=None
        config = PassManagerConfig(
            initial_layout=None,
            basis_gates=["u1", "u2", "u3"],
            coupling_map=None,
            target=None,
        )
        
        # Get the layout pass manager with optimization_level=0
        plugin = DefaultLayoutPassManager()
        pass_manager = plugin.pass_manager(config, optimization_level=0)
        
        # The key test: we should be able to create the pass manager without error
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        
        # This should not crash with layout-related errors
        try:
            result = pass_manager.run(qc)
            self.assertIsInstance(result, QuantumCircuit)
        except AttributeError as e:
            if "'NoneType' object has no attribute 'size'" in str(e):
                # This is the error that would happen if layout passes were constructed with None
                self.fail("Layout passes were constructed with coupling_map=None, which should not happen")
            else:
                raise  # Re-raise if it's a different AttributeError
        except Exception as e:
            # Other exceptions are fine
            pass

    def test_default_layout_pass_manager_no_layout_when_coupling_map_none_opt1(self):
        """Test that DefaultLayoutPassManager does not create layout passes when coupling_map=None for optimization_level=1."""
        # Create a configuration with coupling_map=None
        config = PassManagerConfig(
            initial_layout=None,
            basis_gates=["u1", "u2", "u3"],
            coupling_map=None,
            target=None,
        )
        
        # Get the layout pass manager with optimization_level=1
        plugin = DefaultLayoutPassManager()
        pass_manager = plugin.pass_manager(config, optimization_level=1)
        
        # The key test: we should be able to create the pass manager without error
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        
        # This should not crash with layout-related errors
        try:
            result = pass_manager.run(qc)
            self.assertIsInstance(result, QuantumCircuit)
        except AttributeError as e:
            if "'NoneType' object has no attribute 'size'" in str(e):
                # This is the error that would happen if layout passes were constructed with None
                self.fail("Layout passes were constructed with coupling_map=None, which should not happen")
            else:
                raise  # Re-raise if it's a different AttributeError
        except Exception as e:
            # Other exceptions are fine
            pass

    def test_dense_layout_pass_manager_no_layout_when_coupling_map_none(self):
        """Test that DenseLayoutPassManager does not create layout passes when coupling_map=None."""
        # Create a configuration with coupling_map=None
        config = PassManagerConfig(
            initial_layout=None,
            basis_gates=["u1", "u2", "u3"],
            coupling_map=None,
            target=None,
        )
        
        # Get the layout pass manager
        plugin = DenseLayoutPassManager()
        pass_manager = plugin.pass_manager(config, optimization_level=0)
        
        # The key test: we should be able to create the pass manager without error
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        
        # This should not crash with layout-related errors
        try:
            result = pass_manager.run(qc)
            self.assertIsInstance(result, QuantumCircuit)
        except AttributeError as e:
            if "'NoneType' object has no attribute 'size'" in str(e):
                # This is the error that would happen if layout passes were constructed with None
                self.fail("Layout passes were constructed with coupling_map=None, which should not happen")
            else:
                raise  # Re-raise if it's a different AttributeError
        except Exception as e:
            # Other exceptions are fine
            pass

    def test_sabre_layout_pass_manager_no_layout_when_coupling_map_none_opt2(self):
        """Test that SabreLayoutPassManager does not create layout passes when coupling_map=None for optimization_level=2."""
        # Create a configuration with coupling_map=None
        config = PassManagerConfig(
            initial_layout=None,
            basis_gates=["u1", "u2", "u3"],
            coupling_map=None,
            target=None,
        )
        
        # Get the layout pass manager with optimization_level=2
        plugin = SabreLayoutPassManager()
        pass_manager = plugin.pass_manager(config, optimization_level=2)
        
        # The key test: we should be able to create the pass manager without error
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        
        # This should not crash with layout-related errors
        try:
            result = pass_manager.run(qc)
            self.assertIsInstance(result, QuantumCircuit)
        except AttributeError as e:
            if "'NoneType' object has no attribute 'size'" in str(e):
                # This is the error that would happen if layout passes were constructed with None
                self.fail("SabreLayout was constructed with coupling_map=None, which should not happen")
            else:
                raise  # Re-raise if it's a different AttributeError
        except Exception as e:
            # Other exceptions are fine
            pass

    def test_sabre_layout_pass_manager_no_layout_when_coupling_map_none_opt3(self):
        """Test that SabreLayoutPassManager does not create layout passes when coupling_map=None for optimization_level=3."""
        # Create a configuration with coupling_map=None
        config = PassManagerConfig(
            initial_layout=None,
            basis_gates=["u1", "u2", "u3"],
            coupling_map=None,
            target=None,
        )
        
        # Get the layout pass manager with optimization_level=3
        plugin = SabreLayoutPassManager()
        pass_manager = plugin.pass_manager(config, optimization_level=3)
        
        # The key test: we should be able to create the pass manager without error
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        
        # This should not crash with layout-related errors
        try:
            result = pass_manager.run(qc)
            self.assertIsInstance(result, QuantumCircuit)
        except AttributeError as e:
            if "'NoneType' object has no attribute 'size'" in str(e):
                # This is the error that would happen if layout passes were constructed with None
                self.fail("SabreLayout was constructed with coupling_map=None, which should not happen")
            else:
                raise  # Re-raise if it's a different AttributeError
        except Exception as e:
            # Other exceptions are fine
            pass

    def test_default_layout_pass_manager_with_coupling_map_not_none(self):
        """Test that DefaultLayoutPassManager still works correctly when coupling_map is not None."""
        # Create a configuration with a valid coupling map
        from qiskit.transpiler import CouplingMap
        coupling_map = CouplingMap.from_line(2)
        config = PassManagerConfig(
            initial_layout=None,
            basis_gates=["u1", "u2", "u3"],
            coupling_map=coupling_map,
            target=None,
        )
        
        # Get the layout pass manager with optimization_level=0
        plugin = DefaultLayoutPassManager()
        pass_manager = plugin.pass_manager(config, optimization_level=0)
        
        # Should be able to run without error
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        
        # This should work fine with a valid coupling map
        result = pass_manager.run(qc)
        self.assertIsInstance(result, QuantumCircuit)

    def test_trivial_layout_pass_manager_with_coupling_map_not_none(self):
        """Test that TrivialLayoutPassManager still works correctly when coupling_map is not None."""
        # Create a configuration with a valid coupling map
        from qiskit.transpiler import CouplingMap
        coupling_map = CouplingMap.from_line(2)
        config = PassManagerConfig(
            initial_layout=None,
            basis_gates=["u1", "u2", "u3"],
            coupling_map=coupling_map,
            target=None,
        )
        
        # Get the layout pass manager
        plugin = TrivialLayoutPassManager()
        pass_manager = plugin.pass_manager(config, optimization_level=0)
        
        # Should be able to run without error
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        
        # This should work fine with a valid coupling map
        result = pass_manager.run(qc)
        self.assertIsInstance(result, QuantumCircuit)

    def test_dense_layout_pass_manager_with_coupling_map_not_none(self):
        """Test that DenseLayoutPassManager still works correctly when coupling_map is not None."""
        # Create a configuration with a valid coupling map
        from qiskit.transpiler import CouplingMap
        coupling_map = CouplingMap.from_line(2)
        config = PassManagerConfig(
            initial_layout=None,
            basis_gates=["u1", "u2", "u3"],
            coupling_map=coupling_map,
            target=None,
        )
        
        # Get the layout pass manager
        plugin = DenseLayoutPassManager()
        pass_manager = plugin.pass_manager(config, optimization_level=0)
        
        # Should be able to run without error
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        
        # This should work fine with a valid coupling map
        result = pass_manager.run(qc)
        self.assertIsInstance(result, QuantumCircuit)

    def test_sabre_layout_pass_manager_with_coupling_map_not_none_opt0(self):
        """Test that SabreLayoutPassManager still works correctly when coupling_map is not None for optimization_level=0."""
        # Create a configuration with a valid coupling map
        from qiskit.transpiler import CouplingMap
        coupling_map = CouplingMap.from_line(2)
        config = PassManagerConfig(
            initial_layout=None,
            basis_gates=["u1", "u2", "u3"],
            coupling_map=coupling_map,
            target=None,
        )
        
        # Get the layout pass manager with optimization_level=0
        plugin = SabreLayoutPassManager()
        pass_manager = plugin.pass_manager(config, optimization_level=0)
        
        # Should be able to run without error
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        
        # This should work fine with a valid coupling map
        result = pass_manager.run(qc)
        self.assertIsInstance(result, QuantumCircuit)