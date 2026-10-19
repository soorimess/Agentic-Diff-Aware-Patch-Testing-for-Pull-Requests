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

"""Tests for the Solovay Kitaev decomposition fix for loading from file."""

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


def test_solovay_kitaev_load_from_file_attribute_error():
    """Test that loading basic approximations from file works without AttributeError."""
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(suffix=".npy", delete=False) as tmp_file:
        temp_filename = tmp_file.name

    try:
        # Generate basic approximations and save to file
        generate_basic_approximations(["t", "tdg", "h"], 10, temp_filename)
        
        # This should not raise an AttributeError anymore
        sk_file = SolovayKitaevDecomposition(temp_filename)
        
        # Test that we can actually use the loaded decomposition
        rotation = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
        qc_file = sk_file.run(_convert_so3_to_su2(rotation), 2)
        
        # If we get here without AttributeError, the fix works
        assert qc_file is not None
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_solovay_kitaev_global_phase_preservation():
    """Test that global phase is preserved when loading approximations from file."""
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(suffix=".npy", delete=False) as tmp_file:
        temp_filename = tmp_file.name

    try:
        # Generate basic approximations and save to file
        generate_basic_approximations(["t", "tdg", "h"], 10, temp_filename)
        
        # Create two decomposers - one from file, one from scratch
        sk = SolovayKitaevDecomposition()
        sk_file = SolovayKitaevDecomposition(temp_filename)
        
        # Test with a rotation that should produce different global phases
        # if the bug exists
        rotation = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
        
        qc = sk.run(_convert_so3_to_su2(rotation), 2)
        qc_file = sk_file.run(_convert_so3_to_su2(rotation), 2)
        
        # The global phases should be the same (both should be 0 or both should be π)
        # This tests that the global phase information is preserved when loading from file
        assert qc.global_phase == qc_file.global_phase
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_solovay_kitaev_load_from_dict_with_phase():
    """Test that loading from dictionary with phase information works correctly."""
    # Generate basic approximations to get the data structure
    sequences = generate_basic_approximations(["t", "tdg", "h"], 5, None)
    
    # Create a dictionary like what would be saved to file (with phase info)
    data_dict = {}
    for sequence in sequences:
        gatestring = sequence.name
        # This is how the data should be saved according to the fix
        data_dict[gatestring] = (sequence.product, sequence.global_phase)
    
    # This should work without errors
    sk = SolovayKitaevDecomposition(data_dict)
    
    # Test that we can actually use the decomposition
    rotation = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    qc = sk.run(_convert_so3_to_su2(rotation), 2)
    
    assert qc is not None


def test_solovay_kitaev_load_from_dict_without_phase():
    """Test backwards compatibility with old dictionary format (no phase info)."""
    # Generate basic approximations to get the data structure
    sequences = generate_basic_approximations(["t", "tdg", "h"], 5, None)
    
    # Create a dictionary like the old format (just matrices, no phase info)
    data_dict = {}
    for sequence in sequences:
        gatestring = sequence.name
        # Old format - just the matrix (no global phase)
        data_dict[gatestring] = sequence.product
    
    # This should work without errors (backwards compatibility)
    sk = SolovayKitaevDecomposition(data_dict)
    
    # Test that we can actually use the decomposition
    rotation = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    qc = sk.run(_convert_so3_to_su2(rotation), 2)
    
    assert qc is not None