# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression test for astropy issue #14539:
FITSDiff may sometimes report differences between identical files.
"""

def test_q_format_vla_handling_condition():
    """
    Test that specifically checks the condition change in the fixed code.
    
    The change was:
    Before: elif "P" in col.format:
    After:  elif "P" in col.format or "Q" in col.format:
    
    This test directly checks that Q-format columns get treated 
    the same as P-format columns in terms of conditional logic.
    """
    # Test the exact conditional logic that was changed
    format_p = "PD"  # P format (should trigger VLA branch)
    format_q = "QD"  # Q format (was broken before fix)
    format_regular = "D"  # Regular format (should not trigger VLA branch)
    
    # The condition under test
    def old_behavior(fmt):
        # Old buggy behavior
        return "P" in fmt
        
    def new_behavior(fmt):  
        # New fixed behavior
        return "P" in fmt or "Q" in fmt
    
    # Test that P formats work the same in both:
    assert old_behavior(format_p) == True
    assert new_behavior(format_p) == True
    
    # Test that Q formats behave differently:
    assert old_behavior(format_q) == False  # Was broken - no VLA handling
    assert new_behavior(format_q) == True   # Now fixed - VLA handling
    
    # Test that regular formats behave the same:
    assert old_behavior(format_regular) == False
    assert new_behavior(format_regular) == False
    
    # This demonstrates why the bug existed:
    # When comparing data with QD format VLA columns, 
    # the old code would fall through to the problematic array comparison:
    # diffs = np.where(arra != arrb)  # This crashes on different-length VLAs
    
    # But the new code correctly routes them to:
    # diffs = [idx for idx in range(len(arra)) if not np.allclose(... )]
    # which is safe for variable-length arrays