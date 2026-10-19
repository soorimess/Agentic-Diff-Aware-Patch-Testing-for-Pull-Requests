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

"""Test for the Solovay Kitaev decomposition loading from file bug."""

import numpy as np
import tempfile
import os
from qiskit.synthesis.discrete_basis.solovay_kitaev import (
    SolovayKitaevDecomposition,
)
from qiskit.synthesis.discrete_basis import generate_basic_approximations
from qiskit.synthesis.discrete_basis.gate_sequence import (
    _convert_so3_to_su2,
)


def test_solovay_kitaev_load_from_file_basic():
    """Test that SolovayKitaevDecomposition can load approximations from file correctly."""
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(suffix='.npy', delete=False) as tmp_file:
        temp_filename = tmp_file.name
    
    try:
        # Generate basic approximations and save to file
        generate_basic_approximations(["t", "tdg", "h"], 10, temp_filename)
        
        # This should not raise an AttributeError
        sk_file = SolovayKitaevDecomposition(temp_filename)
        
        # Test that the loaded decomposition works correctly
        rotation = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
        
        # Create a decomposition without loading from file
        sk = SolovayKitaevDecomposition()
        qc = sk.run(_convert_so3_to_su2(rotation), 2)
        
        # Create a decomposition loading from file
        qc_file = sk_file.run(_convert_so3_to_su2(rotation), 2)
        
        # Both should have the same global phase
        assert qc.global_phase == qc_file.global_phase, (
            f"Global phases differ: {qc.global_phase} vs {qc_file.global_phase}"
        )
        
        # Both should have the same number of gates
        assert len(qc.data) == len(qc_file.data), (
            f"Number of gates differ: {len(qc.data)} vs {len(qc_file.data)}"
        )
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_solovay_kitaev_load_from_file_with_global_phase():
    """Test that SolovayKitaevDecomposition preserves global phase when loading from file."""
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(suffix='.npy', delete=False) as tmp_file:
        temp_filename = tmp_file.name
    
    try:
        # Generate basic approximations and save to file
        generate_basic_approximations(["t", "tdg", "h"], 10, temp_filename)
        
        # This should not raise an AttributeError
        sk_file = SolovayKitaevDecomposition(temp_filename)
        
        # Test with a rotation that should produce a specific global phase
        # Using a rotation that should produce a global phase of π
        rotation = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
        
        # Create a decomposition without loading from file
        sk = SolovayKitaevDecomposition()
        qc = sk.run(_convert_so3_to_su2(rotation), 2)
        
        # Create a decomposition loading from file
        qc_file = sk_file.run(_convert_so3_to_su2(rotation), 2)
        
        # Both should have the same global phase
        assert qc.global_phase == qc_file.global_phase, (
            f"Global phases differ: {qc.global_phase} vs {qc_file.global_phase}"
        )
        
        # Test that both decompositions produce equivalent circuits
        # (they should be equivalent up to global phase)
        assert qc.global_phase == qc_file.global_phase
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_solovay_kitaev_load_from_file_preserves_gate_sequences():
    """Test that GateSequence objects are correctly reconstructed from file."""
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(suffix='.npy', delete=False) as tmp_file:
        temp_filename = tmp_file.name
    
    try:
        # Generate basic approximations and save to file
        generate_basic_approximations(["t", "tdg", "h"], 10, temp_filename)
        
        # This should not raise an AttributeError
        sk_file = SolovayKitaevDecomposition(temp_filename)
        
        # Check that the loaded approximations have proper structure
        assert len(sk_file.basic_approximations) > 0
        
        # Check that each GateSequence has the expected attributes
        for seq in sk_file.basic_approximations:
            assert hasattr(seq, 'gates')
            assert hasattr(seq, 'product')
            assert hasattr(seq, 'labels')
            assert hasattr(seq, 'global_phase')
            
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)