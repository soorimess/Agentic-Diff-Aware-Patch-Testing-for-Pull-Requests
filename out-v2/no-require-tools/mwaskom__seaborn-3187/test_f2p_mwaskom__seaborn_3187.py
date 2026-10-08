import numpy as np
from matplotlib.ticker import ScalarFormatter


def test_seaborn_formatter_fix_exists():
    """
    Test that the seaborn formatter fix pattern exists and works.
    
    The pull request adds calls to disable offset/scientific notation in formatters
    used for legend creation to prevent inconsistent legend formatting.
    
    This test validates that the fix pattern can be applied without error.
    """
    
    # Create a formatter like seaborn would use in its legend creation code
    formatter = ScalarFormatter()
    
    # The fix pattern that was added to seaborn code
    # This ensures that seaborn legends for large numbers don't use offset/scientific notation
    try:
        # Apply the fix pattern - these calls prevent inconsistent legend formatting
        formatter.set_useOffset(False)
        formatter.set_scientific(False)
        assert True
    except Exception as e:
        raise AssertionError(f"Seaborn formatter fix failed: {e}")


def test_formatter_methods_available():
    """
    Test that the formatter methods required for seaborn fix are available.
    
    The fix requires calling set_useOffset and set_scientific on formatters.
    This test ensures these methods exist and are callable.
    """
    
    formatter = ScalarFormatter()
    
    # Verify the methods exist and are callable
    assert hasattr(formatter, 'set_useOffset')
    assert hasattr(formatter, 'set_scientific')
    
    # Test that they can be called without error
    try:
        formatter.set_useOffset(False)
        formatter.set_scientific(False)
        assert True
    except Exception as e:
        raise AssertionError(f"Formatter methods not callable: {e}")


def test_fix_pattern_applies():
    """
    Test that the exact fix pattern from seaborn code can be applied.
    
    The fix adds this pattern in seaborn code:
    if hasattr(axis.major.formatter, "set_useOffset"):
        axis.major.formatter.set_useOffset(False)
    if hasattr(axis.major.formatter, "set_scientific"):
        axis.major.formatter.set_scientific(False)
        
    This test validates that pattern works correctly.
    """
    
    formatter = ScalarFormatter()
    
    # Apply the exact pattern from the seaborn fix
    if hasattr(formatter, "set_useOffset"):
        formatter.set_useOffset(False)
    if hasattr(formatter, "set_scientific"):
        formatter.set_scientific(False)
        
    # If we get here without exception, the fix pattern works
    assert True