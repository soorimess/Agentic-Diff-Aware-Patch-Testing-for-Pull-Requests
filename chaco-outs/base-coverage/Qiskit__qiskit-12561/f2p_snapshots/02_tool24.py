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

"""Test for regression of issue #12541 and PR #12561."""

from qiskit.circuit import ParameterVector


def test_parametervector_resize_truncates_params():
    """Test that ParameterVector.resize() properly truncates params to current size."""
    # Create a ParameterVector with 20 elements
    pv = ParameterVector("theta", 20)
    
    # Verify initial state
    assert len(pv.params) == 20
    assert len(pv) == 20
    
    # Resize to 3 elements
    pv.resize(3)
    
    # After resize, params should only contain the current elements
    # This is the main fix: before the fix, params would still have 20 elements
    assert len(pv.params) == 3, f"Expected 3 params, got {len(pv.params)}"
    
    # The elements should be the same objects
    assert pv.params[0] is pv[0]
    assert pv.params[1] is pv[1]
    assert pv.params[2] is pv[2]


def test_parametervector_index_raises_for_old_elements():
    """Test that ParameterVector.index() raises ValueError for elements not in current vector."""
    # Create a ParameterVector with 20 elements
    pv = ParameterVector("theta", 20)
    
    # Get the last element
    last = pv[-1]
    
    # Resize to 3 elements
    pv.resize(3)
    
    # After resize, indexing the old element should raise ValueError
    # This is the main issue reported: index() was returning old indices instead of raising errors
    try:
        pv.index(last)
        # If we get here, it means the old behavior still exists
        assert False, "Expected ValueError when indexing element not in resized vector"
    except ValueError:
        # This is the expected behavior after the fix
        pass


def test_parametervector_len_returns_actual_length():
    """Test that ParameterVector.__len__() returns actual length of params."""
    # Create a ParameterVector with 20 elements
    pv = ParameterVector("theta", 20)
    
    # Resize to 3 elements
    pv.resize(3)
    
    # len() should return the actual number of elements
    assert len(pv) == 3


def test_parametervector_string_representation():
    """Test that ParameterVector string representation only shows current elements."""
    # Create a ParameterVector with 20 elements
    pv = ParameterVector("theta", 20)
    
    # Resize to 3 elements
    pv.resize(3)
    
    # String representation should only show current elements
    str_repr = str(pv)
    assert "theta" in str_repr
    
    # Should contain exactly 3 parameter names
    param_names = [str(p) for p in pv.params]
    for name in param_names:
        assert name in str_repr
    
    # Should not contain names of old elements
    assert "theta[19]" not in str_repr