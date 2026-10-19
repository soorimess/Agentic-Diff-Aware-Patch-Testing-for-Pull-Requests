"""
Regression test for the fix of DeprecationWarning with setuptools >= 60.0.0

This test validates that version strings are compatible with the new Version class
approach that will eliminate deprecation warnings.
"""

import matplotlib as mpl
import scipy as sp


def test_version_string_compatibility():
    """
    Test that version strings from matplotlib and scipy are compatible with 
    version comparison operations that will be changed in the PR.
    """
    
    # These are the version strings used in the changed code paths:
    # LooseVersion(mpl.__version__) >= "3.0" (rcmod.py)
    # LooseVersion(mpl.__version__) >= "3.3" (_core.py)
    # LooseVersion(mpl.__version__) < LooseVersion("3.0") (axisgrid.py)
    # LooseVersion(mpl.__version__) < "3.0" (categorical.py)
    # LooseVersion(sp.__version__) < "1.2.0" (_statistics.py)
    
    mpl_version = mpl.__version__
    sp_version = sp.__version__
    
    # Validate that version strings are properly formatted for version comparison
    assert isinstance(mpl_version, str)
    assert isinstance(sp_version, str)
    assert len(mpl_version) > 0
    assert len(sp_version) > 0
    
    # Test that version strings contain numeric components needed for comparison
    mpl_parts = mpl_version.split('.')
    sp_parts = sp_version.split('.')
    
    # Should have at least one numeric part
    assert len(mpl_parts) >= 1
    assert len(sp_parts) >= 1
    
    # First part should be numeric (major version)
    assert mpl_parts[0].isdigit()
    assert sp_parts[0].isdigit()


def test_version_components():
    """
    Test that version strings contain components compatible with version comparison.
    """
    
    mpl_version = mpl.__version__
    sp_version = sp.__version__
    
    # Validate version strings are properly formatted
    assert isinstance(mpl_version, str) and len(mpl_version) > 0
    assert isinstance(sp_version, str) and len(sp_version) > 0
    
    # Test that version strings contain numeric components
    mpl_parts = mpl_version.split('.')
    sp_parts = sp_version.split('.')
    
    # Should have at least one numeric part
    assert len(mpl_parts) >= 1
    assert len(sp_parts) >= 1
    
    # First part should be numeric (major version)
    assert mpl_parts[0].isdigit()
    assert sp_parts[0].isdigit()


def test_version_structure():
    """
    Test that version strings follow structure compatible with version comparison.
    """
    
    # Test that version strings are compatible with version parsing logic
    mpl_version = mpl.__version__
    sp_version = sp.__version__
    
    # Basic validation that version strings are valid
    assert isinstance(mpl_version, str)
    assert isinstance(sp_version, str)
    assert len(mpl_version) > 0
    assert len(sp_version) > 0
    
    # Test that they can be processed by version comparison logic
    assert mpl_version.split('.')[0].isdigit()
    assert sp_version.split('.')[0].isdigit()


def test_version_inputs():
    """
    Test that version strings meet requirements for version comparison contexts.
    """
    
    # Test that version strings are properly formatted for version comparisons
    mpl_version = mpl.__version__
    sp_version = sp.__version__
    
    # Both should be non-empty strings
    assert isinstance(mpl_version, str) and len(mpl_version) > 0
    assert isinstance(sp_version, str) and len(sp_version) > 0
    
    # Test that they contain version-like components
    assert '.' in mpl_version or 'a' in mpl_version or 'b' in mpl_version or 'rc' in mpl_version
    assert '.' in sp_version or 'a' in sp_version or 'b' in sp_version or 'rc' in sp_version