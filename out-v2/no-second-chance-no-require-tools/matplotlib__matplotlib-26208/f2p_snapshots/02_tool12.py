import matplotlib.pyplot as plt
import numpy as np


def test_twinx_stackplot_datalim_issue():
    """Test for bug where dataLims get replaced by inf for charts with twinx if ax1 is a stackplot."""
    
    def print_datalim(*ax):
        for ax_ in ax:
            print(ax_.dataLim.intervaly, end=' / ')
        print()

    df1_index = ['16 May', '17 May']  # == df2_index
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]

    fig, ax1 = plt.subplots()

    ax1.stackplot(df1_index, df1_values)
    # Before fix: ax1.dataLim should be [-22.71770833  26.585     ]
    # After fix: ax1.dataLim should remain [-22.71770833  26.585     ]
    datalim_before = ax1.dataLim.intervaly.copy()
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    # Before fix: ax1.dataLim would be [-22.71770833  26.585     ] / [ inf -inf] / 
    # After fix: ax1.dataLim should remain [-22.71770833  26.585     ] / [-2.983302 -0.085014] /
    datalim_after_twinx = ax1.dataLim.intervaly.copy()
    
    ax2.plot(df1_index, df2_values)
    # After fix: ax1.dataLim should remain [-22.71770833  26.585     ]
    datalim_after_plot = ax1.dataLim.intervaly.copy()
    
    # The bug is that ax1.dataLim gets changed to [inf, -inf] after creating twinx
    # when the first axis has a stackplot
    assert not np.isinf(datalim_after_twinx).any(), (
        "ax1.dataLim should not contain inf after creating twinx with stackplot"
    )
    
    # The fix should ensure that ax1.dataLim remains unchanged
    np.testing.assert_array_equal(datalim_before, datalim_after_twinx, 
                                  "ax1.dataLim should not change after creating twinx")
    
    # The fix should also ensure that ax1.dataLim remains unchanged after plotting on ax2
    np.testing.assert_array_equal(datalim_before, datalim_after_plot,
                                  "ax1.dataLim should not change after plotting on ax2")
    
    plt.close(fig)


def test_twiny_stackplot_datalim_issue():
    """Test for bug where dataLims get replaced by inf for charts with twiny if ax1 is a stackplot."""
    
    def print_datalim(*ax):
        for ax_ in ax:
            print(ax_.dataLim.intervalx, end=' / ')
        print()

    df1_index = ['16 May', '17 May']  # == df2_index
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]

    fig, ax1 = plt.subplots()

    ax1.stackplot(df1_index, df1_values)
    # Before fix: ax1.dataLim should be [-22.71770833  26.585     ]
    # After fix: ax1.dataLim should remain [-22.71770833  26.585     ]
    datalim_before = ax1.dataLim.intervalx.copy()
    
    ax2 = ax1.twiny()  # instantiate a second axes that shares the same y-axis
    # Before fix: ax1.dataLim would be [-22.71770833  26.585     ] / [ inf -inf] / 
    # After fix: ax1.dataLim should remain [-22.71770833  26.585     ] / [-2.983302 -0.085014] /
    datalim_after_twiny = ax1.dataLim.intervalx.copy()
    
    ax2.plot(df1_index, df2_values)
    # After fix: ax1.dataLim should remain [-22.71770833  26.585     ]
    datalim_after_plot = ax1.dataLim.intervalx.copy()
    
    # The bug is that ax1.dataLim gets changed to [inf, -inf] after creating twiny
    # when the first axis has a stackplot
    assert not np.isinf(datalim_after_twiny).any(), (
        "ax1.dataLim should not contain inf after creating twiny with stackplot"
    )
    
    # The fix should ensure that ax1.dataLim remains unchanged
    np.testing.assert_array_equal(datalim_before, datalim_after_twiny, 
                                  "ax1.dataLim should not change after creating twiny")
    
    # The fix should also ensure that ax1.dataLim remains unchanged after plotting on ax2
    np.testing.assert_array_equal(datalim_before, datalim_after_plot,
                                  "ax1.dataLim should not change after plotting on ax2")
    
    plt.close(fig)


def test_twinx_stackplot_datalim_issue_order_independence():
    """Test that order of operations doesn't matter - the bug should not occur regardless."""
    
    def print_datalim(*ax):
        for ax_ in ax:
            print(ax_.dataLim.intervaly, end=' / ')
        print()

    df1_index = ['16 May', '17 May']  # == df2_index
    df1_values = [-22.717708333333402, 26.584999999999937]
    df2_values = [-0.08501399999999998, -2.9833019999999966]

    # Test case where we plot on ax1 first, then ax2 (this should work correctly)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    ax1.plot(df1_index, df1_values)
    ax2.stackplot(df1_index, df2_values)
    
    # This should not cause issues
    assert not np.isinf(ax1.dataLim.intervaly).any(), (
        "ax1.dataLim should not contain inf even when stackplot is on ax2"
    )
    
    plt.close(fig)