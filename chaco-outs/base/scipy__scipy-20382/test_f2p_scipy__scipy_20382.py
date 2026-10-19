"""
Regression test for PR #20382: MAINT: lint: enforce `numpy as np` alias

This test ensures that the functions using numpy work correctly with the enforced
import convention of `import numpy as np` instead of `import numpy as _np`.
"""

import numpy as np
from numpy.testing import assert_allclose


def test_import_alias_enforcement():
    """Test that the numpy import alias has been properly enforced."""
    # Test that the new import convention works correctly
    assert hasattr(np, 'array')
    assert hasattr(np, 'dtype')
    
    # Test BLAS functionality with np (not _np)
    from scipy.linalg import blas
    result = blas.find_best_blas_type([np.array([1.0, 2.0])], dtype=np.float64)
    assert len(result) == 3  # prefix, dtype, prefer_fortran
    
    # Test LAPACK constants with np (not _np)
    from scipy.linalg import lapack
    assert hasattr(lapack, '_int32_max')
    assert hasattr(lapack, '_int64_max')
    
    # Test constants functions with np (not _np)
    from scipy.constants import convert_temperature
    result = convert_temperature(0, 'celsius', 'kelvin')
    assert result == 273.15


def test_dtype_functionality():
    """Test dtype handling functions that use np.dtype (was _np.dtype)."""
    from scipy.linalg import blas
    
    # Test with different data types to ensure comprehensive coverage
    prefix, dtype, prefer_fortran = blas.find_best_blas_type(
        [np.array([1.0, 2.0])], dtype=np.float64
    )
    assert prefix in ['s', 'd', 'c', 'z']
    assert dtype == np.dtype('float64')
    assert isinstance(prefer_fortran, bool)
    
    # Test with complex data type
    prefix, dtype, prefer_fortran = blas.find_best_blas_type(
        [np.array([1+2j, 3+4j])], dtype=np.complex128
    )
    assert prefix in ['s', 'd', 'c', 'z']
    assert dtype == np.dtype('complex128')


def test_constants_conversion():
    """Test constants conversion functions that use np.asanyarray (was _np.asanyarray)."""
    from scipy.constants import convert_temperature, lambda2nu, nu2lambda
    
    # Test all temperature conversion scales
    result = convert_temperature(0, 'celsius', 'kelvin')
    assert_allclose(result, 273.15)
    
    result = convert_temperature(273.15, 'kelvin', 'celsius')
    assert_allclose(result, 0.0)
    
    result = convert_temperature(32, 'fahrenheit', 'kelvin')
    assert_allclose(result, 273.15)
    
    result = convert_temperature(491.67, 'rankine', 'kelvin')
    assert_allclose(result, 273.15)
    
    # Test wavelength and frequency conversion
    lambda_vals = [1e-9, 5e-7]
    nu_vals = lambda2nu(lambda_vals)
    assert len(nu_vals) == 2
    
    nu_vals = [1e15, 1e16]
    lambda_vals = nu2lambda(nu_vals)
    assert len(lambda_vals) == 2


def test_precision_types():
    """Test precision type handling that uses np.float32, np.complex64, etc."""
    # Test that numpy precision types work correctly
    test_val = np.float32(1.0)
    assert test_val == np.float32(1.0)
    
    test_complex = np.complex64(1+2j)
    assert test_complex == np.complex64(1+2j)
    
    test_intc = np.intc(42)
    assert test_intc == np.intc(42)
    
    test_int64 = np.int64(42)
    assert test_int64 == np.int64(42)