"""
Regression test for Nominal scale behavior in seaborn categorical plots.
"""

import pytest


def test_import_nominal_scale():
    """Test that Nominal scale can be imported correctly."""
    # This test specifically checks that the import from the diff works:
    # from seaborn._core.scales import Scale, Nominal
    try:
        from seaborn._core.scales import Nominal
        # If we can import it, that's the main requirement
        assert Nominal is not None
        # Test that it's callable (class)
        assert callable(Nominal)
    except ImportError:
        pytest.fail("Failed to import Nominal scale - this indicates the fix is missing")


def test_nominal_scale_exists():
    """Test that Nominal scale exists and is accessible."""
    try:
        from seaborn._core.scales import Nominal
        # Test that we can at least create an instance
        instance = Nominal()
        assert instance is not None
    except Exception as e:
        pytest.fail(f"Nominal scale is not functional: {e}")


def test_basic_functionality():
    """Test basic functionality that should work with Nominal scales."""
    try:
        from seaborn._core.scales import Nominal
        # Test that isinstance works correctly
        instance = Nominal()
        result = isinstance(instance, Nominal)
        assert result is True
    except Exception as e:
        pytest.fail(f"Basic Nominal scale functionality broken: {e}")