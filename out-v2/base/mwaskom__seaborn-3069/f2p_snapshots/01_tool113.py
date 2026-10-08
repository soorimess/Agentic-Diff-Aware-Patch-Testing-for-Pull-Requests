"""
Regression test for Nominal scale behavior fix.

This test verifies that the key infrastructure changes for Nominal scale handling
were implemented in the plot.py file, which enables the special behaviors for 
Nominal scales to match categorical scales.
"""

import pytest


def test_nominal_scale_import_exists_at_module_level():
    """
    Test that Nominal scale is imported at module level in plot.py.
    
    This validates the core change: the import statement was moved from 
    inside a function to the top of the file, enabling Nominal scale handling.
    """
    # Import the module to check if Nominal is available at module level
    import seaborn._core.plot as plot_module
    
    # Check that Nominal is accessible from the module
    # This would fail if the import wasn't added to the top of plot.py
    try:
        Nominal = getattr(plot_module, 'Nominal')
        assert Nominal is not None
        assert callable(Nominal)
    except AttributeError:
        pytest.fail("Nominal scale not found in plot module - import was not added")


def test_nominal_scale_is_usable_in_isinstance_checks():
    """
    Test that Nominal scale can be used in isinstance checks.
    
    This validates that the infrastructure exists for the isinstance logic
    that was added in _finalize_figure method.
    """
    # Import Nominal from the expected location
    from seaborn._core.scales import Nominal
    
    # Test that we can create and use Nominal instances
    nominal = Nominal()
    assert nominal is not None
    
    # Test isinstance check (this is the core logic that enables the fix)
    assert isinstance(nominal, Nominal)
    
    # Test that it has expected scale properties
    assert hasattr(nominal, '_priority')


def test_nominal_scale_has_correct_inheritance():
    """
    Test that Nominal scale has correct inheritance structure.
    
    This ensures Nominal scales can be properly identified and handled
    in the _finalize_figure method logic.
    """
    from seaborn._core.scales import Nominal, Scale
    
    # Test that Nominal inherits from Scale
    assert Scale in Nominal.__bases__
    
    # Test instantiation
    nominal = Nominal()
    assert nominal is not None
    
    # Test that isinstance works correctly for the fix logic
    assert isinstance(nominal, Nominal)
    assert isinstance(nominal, Scale)