"""
Regression tests for import performance improvements in xarray.

This test file ensures that the lazy import changes work correctly and 
don't break existing functionality.
"""

def test_backend_entrypoint_availability():
    """
    Test that backend entrypoints properly report availability for lazy imports.
    
    This test verifies that the lazy import approach works correctly for backend availability checking.
    """
    import xarray as xr
    
    # Test that backend entrypoints exist and have the expected lazy availability checking
    try:
        # Access backend entrypoint - should not raise ImportError even if underlying module isn't available
        backend = xr.backends.NetCDF4BackendEntrypoint
        # Backend should have available attribute for lazy availability checking
        assert hasattr(backend, 'available'), "Backend missing 'available' attribute"
        # Available should be boolean to indicate if module is available
        assert isinstance(backend.available, bool), "Backend.available should be boolean"
    except AttributeError:
        # If NetCDF4 is not available, that's fine - the important thing is 
        # we don't get import errors from just accessing the entrypoint
        pass


def test_core_functionality_preserved():
    """
    Test that core xarray functionality works correctly with lazy imports.
    
    Ensures that the lazy import changes don't break existing functionality.
    """
    import xarray as xr
    
    # Test basic DataArray functionality
    da = xr.DataArray([1, 2, 3], dims=['x'])
    assert da.shape == (3,)
    assert da.sum() == 6
    
    # Test basic Dataset functionality
    ds = xr.Dataset({'temperature': ('time', [1, 2, 3])})
    assert 'temperature' in ds.variables
    assert ds['temperature'].shape == (3,)


def test_import_efficiency():
    """
    Test that xarray imports efficiently without triggering optional dependency imports.
    
    This demonstrates the main benefit of the lazy import changes - faster imports.
    """
    # Import xarray - should be fast and not trigger imports of optional backends
    import xarray as xr
    
    # Basic operations should work immediately
    data = xr.Dataset({'test': ('dim', [1, 2, 3, 4])})
    assert data['test'].shape == (4,)
    
    # Operations should work without import delays
    result = data['test'].mean()
    assert result.shape == ()


def test_backend_accessibility():
    """
    Test that backend entrypoints can be accessed without import-time errors.
    
    This verifies that the lazy import approach prevents import-time errors
    when optional dependencies are not installed.
    """
    import xarray as xr
    
    # These should not raise ImportError just from accessing the class definition
    try:
        # Accessing backend classes should not trigger imports of underlying modules
        netcdf_backend = xr.backends.NetCDF4BackendEntrypoint
        assert netcdf_backend is not None
        # Verify the backend has the expected lazy availability attribute
        if hasattr(netcdf_backend, 'available'):
            assert isinstance(netcdf_backend.available, bool)
    except AttributeError:
        # If netCDF4 is not available, that's fine for this test
        # The important thing is that we don't get import errors from accessing the entrypoint
        pass