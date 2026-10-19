"""
Regression test for hi-res plot directive functionality.

This test verifies the behavior that will be added by the pull request
that enables hi-res plot directive support through the plot_srcset option.
"""

import pytest
import tempfile
import os
from pathlib import Path

pytest.importorskip('sphinx', minversion='4.1.3')


def test_plot_directive_setup_will_add_plot_srcset_config():
    """
    Test that plot directive setup function will add plot_srcset config option.
    
    This test verifies that after the PR, the plot directive setup function
    will properly handle the plot_srcset configuration option.
    """
    # Check that the setup function in plot_directive.py will include the 
    # app.add_config_value('plot_srcset', [], True) line that is added by the PR
    
    import inspect
    from matplotlib.sphinxext.plot_directive import setup
    
    # Get the source of the setup function
    source = inspect.getsource(setup)
    
    # The PR adds: app.add_config_value('plot_srcset', [], True)
    # After the PR, this line should be present
    # So this assertion should FAIL in current state (before PR) and PASS after PR
    assert "plot_srcset" in source, "plot_srcset config should be added by the PR"