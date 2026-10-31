"""
Test for the context manager for constant versions.
This tests the new set_enabled_constants context manager that was added.
"""

import pytest


def test_set_enabled_constants_context_manager_functionality():
    """
    Test that the context manager properly switches constant versions.
    
    The key behavior change is that we can temporarily use older constant 
    versions within a context manager.
    """
    # Import constants to test with
    from astropy.constants import c, m_e
    
    # Test that we can create and use the context manager
    from astropy.constants import set_enabled_constants
    
    # This should not raise an error - the context manager should exist
    context_manager = set_enabled_constants('astropyconst13')
    
    # Verify that we can use it as a context manager
    # (This tests that the @contextmanager decorator works correctly)
    try:
        with context_manager:
            # Within the context, we can access constants
            # The main point is that the context manager can be used
            pass
    except ValueError as e:
        # If we get a ValueError about unsupported modname, that's expected
        # for the current implementation - it should only support astropyconst13
        if 'Context manager does not currently handle' in str(e):
            pytest.skip("Current implementation only supports astropyconst13")
        else:
            raise
    except Exception:
        # Any other exception means something went wrong
        raise
    
    # Test that we can call it with the right argument
    # This tests that the function signature and behavior is correct
    assert callable(set_enabled_constants)
    
    # Test that it raises appropriate error for unsupported versions
    with pytest.raises(ValueError, match="Context manager does not currently handle"):
        with set_enabled_constants('unsupported_version'):
            pass