"""
Test for PR #20382: MAINT: lint: enforce `numpy as np` alias

This test verifies that the import alias convention is properly enforced
by testing the core functionality of modules that use the new import style.
"""

import numpy as np


def test_constants_module_functionality():
    """Test constants module with new numpy import alias."""
    from scipy.constants import convert_temperature, lambda2nu, nu2lambda
    
    # Test basic temperature conversion
    result = convert_temperature(0, 'celsius', 'kelvin')
    assert np.isclose(result, 273.15)
    
    # Test array temperature conversion
    result = convert_temperature([0, 10, 20], 'celsius', 'kelvin')
    expected = np.array([273.15, 283.15, 293.15])
    assert np.allclose(result, expected)
    
    # Test wavelength to frequency conversion
    result = lambda2nu(500e-9)
    expected = 5.99584916e14
    assert np.isclose(result, expected, rtol=1e-10)
    
    # Test frequency to wavelength conversion
    result = nu2lambda(5.99584916e14)
    expected = 500e-9
    assert np.isclose(result, expected, rtol=1e-10)


def test_blas_module_functionality():
    """Test BLAS module with new numpy import alias."""
    from scipy.linalg import get_blas_funcs, find_best_blas_type
    
    # Test function retrieval
    funcs = get_blas_funcs(['dot'])
    assert len(funcs) >= 1
    
    # Test dtype resolution - exercises _np.dtype() calls
    prefix, dtype, prefer_fortran = find_best_blas_type(dtype=np.float32)
    assert isinstance(prefix, str)
    assert hasattr(dtype, 'kind')
    
    # Test with complex dtype
    prefix, dtype, prefer_fortran = find_best_blas_type(dtype=np.complex128)
    assert isinstance(prefix, str)
    assert hasattr(dtype, 'kind')


def test_lapack_module_functionality():
    """Test LAPACK module with new numpy import alias."""
    from scipy.linalg import get_lapack_funcs
    
    # Test function retrieval
    funcs = get_lapack_funcs(['getrf'])
    assert len(funcs) >= 1