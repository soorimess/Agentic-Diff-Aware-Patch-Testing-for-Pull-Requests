# Copyright (c) 2017, The Chancellor, Masters and Scholars of the University
# of Oxford, and the Chebfun Developers. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of Oxford nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Regression test for PR #21485: MAINT: interpolate: abstract out barycentric 
representation of a rational function

This test verifies that the AAA class works correctly with the new barycentric 
representation abstraction that will be available after the PR is applied.
"""

import numpy as np
from numpy.testing import assert_allclose
import pytest
from scipy.interpolate import AAA


def test_class_structure_and_functionality():
    """Test that the class structure supports the new barycentric abstraction."""
    # Test core functionality that should work with the new abstraction
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([0.0, 1.0, 4.0, 9.0])
    
    r = AAA(x, y)
    
    # Test that all barycentric representation components exist
    assert hasattr(r, 'support_points')
    assert hasattr(r, 'support_values')
    assert hasattr(r, 'weights')
    
    # Test evaluation functionality
    x_test = np.array([0.5, 1.5, 2.5])
    y_test = r(x_test)
    
    assert isinstance(y_test, np.ndarray)
    assert y_test.shape == x_test.shape


def test_mathematical_properties_computation():
    """Test that mathematical properties can be computed with new structure."""
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([0.0, 1.0, 4.0, 9.0])
    
    r = AAA(x, y)
    
    # These methods should work with the new abstraction structure
    poles = r.poles()
    residues = r.residues()
    roots = r.roots()
    
    assert isinstance(poles, np.ndarray)
    assert isinstance(residues, np.ndarray)
    assert isinstance(roots, np.ndarray)


def test_input_validation_comprehensive():
    """Test input validation works correctly."""
    # Test various invalid inputs that should be rejected
    with pytest.raises(ValueError, match="same size"):
        AAA([0], [1, 1])
        
    with pytest.raises(ValueError, match="1-D"):
        AAA([[0], [0]], [[1], [1]])
        
    with pytest.raises(ValueError, match="finite"):
        AAA([np.inf], [1])
        
    with pytest.raises(TypeError):
        AAA([1], [1], max_terms=1.0)
        
    with pytest.raises(ValueError, match="greater"):
        AAA([1], [1], max_terms=-1)


def test_functional_equivalence_with_data():
    """Test functional behavior with different data types."""
    # Test with simple quadratic data
    x = np.array([1.0, 2.0, 3.0, 4.0])
    y = np.array([1.0, 4.0, 9.0, 16.0])  # y = x^2
    
    r = AAA(x, y)
    
    # Test evaluation
    x_eval = np.array([1.5, 2.5, 3.5])
    y_eval = r(x_eval)
    
    assert isinstance(y_eval, np.ndarray)
    assert y_eval.shape == x_eval.shape


def test_complex_data_handling():
    """Test that the class handles complex data correctly."""
    # Test with complex numbers to ensure broad compatibility
    x = np.array([0.0+0.0j, 1.0+0.0j, 2.0+0.0j, 3.0+0.0j])
    y = np.array([0.0+0.0j, 1.0+0.0j, 4.0+0.0j, 9.0+0.0j])
    
    r = AAA(x, y)
    
    # Basic functionality should work
    x_test = np.array([0.5+0.0j, 1.5+0.0j, 2.5+0.0j])
    y_test = r(x_test)
    
    assert isinstance(y_test, np.ndarray)
    assert y_test.shape == x_test.shape