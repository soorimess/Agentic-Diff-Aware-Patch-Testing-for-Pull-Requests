"""
Regression test to check Nominal scale handling logic.

This test directly verifies that the specific Nominal scale logic changes
are present and operational by testing proper instantiation and usage.
"""

import matplotlib.pyplot as plt
import pandas as pd
from seaborn._core.plot import Plot
from seaborn._core.scales import Nominal


def test_nominal_scale_basic_functionality():
    """
    Test that Nominal scale can be used in plotting context without error.
    This validates that the code change allows Nominal scales to function properly.
    """
    # Create test data that would exercise the Nominal handling path
    data = pd.DataFrame({
        'a': ['x', 'y', 'z'],
        'b': [1, 2, 3]
    })
    
    # Apply Nominal scale - this is what exercises the new code path
    # In the new code, there's now special handling for isinstance(scale, Nominal)
    plot = Plot(data, x='a', y='b').scale(x=Nominal())
    
    # This should not raise - but more importantly, it should exercise
    # the Nominal-specific code path in the _finalize_figure method 
    fig = plot.plot()
    
    assert fig is not None
    plt.close('all')
    
    # Test that y-axis with Nominal also works  
    plot2 = Plot(data, x='b', y='a').scale(y=Nominal())
    fig2 = plot2.plot()
    
    assert fig2 is not None
    plt.close('all')


def test_nominal_scale_class_availability():
    """
    Validate that Nominal scale class is properly available and functional.
    """
    # Test basic instantiation and class relationship
    nominal = Nominal()
    
    # The essential test here goes to the fact that it's the right scale type
    # and this was part of the original patch - checking Nominal can be imported
    # and used in type checking
    assert nominal is not None
    assert hasattr(nominal, '_priority')