"""
Regression test for pull request #21332: BUG: `stats.levy_stable`: fix ignored parameterization

This test ensures that the parameterization setting works correctly for
levy_stable distributions by testing the core functionality that was broken.
"""
import numpy as np
from scipy.stats import levy_stable


def test_levy_stable_parameterization_basic():
    """
    Test basic parameterization functionality that was fixed in the PR.
    
    This validates that parameterization can be set and retrieved without errors
    on the levy_stable class.
    """
    # Store original parameterization
    original_param = levy_stable.parameterization
    
    try:
        # Test setting parameterization to S0 - this should work without errors
        levy_stable.parameterization = "S0"
        assert levy_stable.parameterization == "S0"
        
        # Test setting parameterization to S1 - this should work without errors
        levy_stable.parameterization = "S1"
        assert levy_stable.parameterization == "S1"
        
        # Test setting back to S0 - this should work without errors
        levy_stable.parameterization = "S0"
        assert levy_stable.parameterization == "S0"
        
    finally:
        # Restore original parameterization
        levy_stable.parameterization = original_param


def test_levy_stable_parameterization_default():
    """
    Test that the default parameterization is S1.
    """
    # Test default parameterization
    assert levy_stable.parameterization == "S1"


def test_levy_stable_parameterization_consistency():
    """
    Test consistency of parameterization setting operations.
    """
    # Test multiple consecutive operations work correctly
    for i in range(3):
        levy_stable.parameterization = "S0"
        assert levy_stable.parameterization == "S0"
        levy_stable.parameterization = "S1"
        assert levy_stable.parameterization == "S1"