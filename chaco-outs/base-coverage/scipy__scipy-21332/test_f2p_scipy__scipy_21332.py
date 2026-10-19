"""
Regression test for PR #21332: BUG: `stats.levy_stable`: fix ignored parameterization
"""

import numpy as np
from scipy.stats import levy_stable


def test_levy_stable_parameterization_bug():
    """
    Test that demonstrates the parameterization bug.
    
    This test verifies that when parameterization is set on the class and
    rvs() is called on an instance, the parameterization should affect the result.
    """
    # Create a stable distribution instance 
    stable_distribution = levy_stable(alpha=1.9, beta=0.1, loc=0.0, scale=1.0)
    
    # Set parameterization to S0 and generate samples
    levy_stable.parameterization = "S0"
    samples_s0 = stable_distribution.rvs(size=(10, 1), random_state=42)
    
    # Set parameterization to S1 and generate samples  
    levy_stable.parameterization = "S1"
    samples_s1 = stable_distribution.rvs(size=(10, 1), random_state=42)
    
    # The bug: samples are identical when they should be different
    # This assertion correctly captures the expected behavior after the fix
    # In the buggy version, this assertion will fail (samples are equal)
    # In the fixed version, this assertion will pass (samples are different)
    assert not np.allclose(samples_s0, samples_s1), (
        "Parameterization setting should affect instance behavior. "
        "Different parameterizations should produce different samples."
    )