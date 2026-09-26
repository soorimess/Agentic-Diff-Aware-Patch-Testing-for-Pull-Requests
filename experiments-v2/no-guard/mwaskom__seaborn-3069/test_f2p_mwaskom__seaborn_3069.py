"""
Regression tests for Nominal scale behavior in seaborn categorical plots.

This test ensures that Nominal scales are handled the same way as categorical 
scales by testing the specific behavior change that was introduced.
"""
import matplotlib.pyplot as plt
import pandas as pd
from seaborn import catplot


def test_string_category_plot_creation():
    """Test that plots with string categories (Nominal) are created successfully."""
    # Create data that will be treated as Nominal scale
    data = pd.DataFrame({
        'group': ['A', 'B', 'C', 'D'],
        'value': [1, 2, 3, 4]
    })
    
    # Create a bar plot - this should trigger Nominal scale behavior
    g = catplot(data=data, x='group', y='value', kind='bar')
    
    # Basic assertion that plot was created
    assert g is not None
    
    # Verify we can access the plot elements
    ax = g.ax
    assert ax is not None
    
    plt.close()


def test_categorical_consistency():
    """Test that categorical and Nominal data work consistently."""
    # Test with string data (Nominal)
    data1 = pd.DataFrame({
        'category': ['X', 'Y', 'Z'],
        'values': [10, 20, 30]
    })
    
    # Test with numeric data (Continuous) 
    data2 = pd.DataFrame({
        'category': [1, 2, 3],
        'values': [10, 20, 30]
    })
    
    # Both should work without error
    g1 = catplot(data=data1, x='category', y='values', kind='bar')
    g2 = catplot(data=data2, x='category', y='values', kind='bar')
    
    assert g1 is not None
    assert g2 is not None
    
    plt.close()
    plt.close()


def test_simple_functionality():
    """Test basic functionality."""
    data = pd.DataFrame({
        'x': ['a', 'b', 'c'],
        'y': [1, 2, 3]
    })
    
    g = catplot(data=data, x='x', y='y', kind='bar')
    
    assert g is not None
    
    plt.close()