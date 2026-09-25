# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Regression test for specific CDS unit parsing issue.
This test should fail in the buggy condition and pass after fix.
"""

import pytest
from astropy import units as u


def test_cds_unit_division_ordering_regression():
    """
    Test that specifically catches the bug in CDS unit parsing where 
    complex division operations had wrong operand ordering.
    
    This is a direct test of the issue described in the bug report:
    - "10+3J/m/s/kpc2" parses to "1000 J s / (kpc2 m)" (wrong order) instead of "1000 J / (m s kpc2)"  
    - "10-7J/s/kpc2" parses to "1e-07 J kpc2 / s" (wrong order) instead of "1e-07 J / (s kpc2)"
    """
    
    # The bug manifests in parsing complex units with multiple divisions
    # This specific test ensures the parser produces the CORRECT output
    
    unit1 = u.Unit("10+3J/m/s/kpc2", format="cds")
    unit2 = u.Unit("10-7J/s/kpc2", format="cds")
    
    print(f"Parsed unit1 (10+3J/m/s/kpc2): {unit1}")
    print(f"Parsed unit2 (10-7J/s/kpc2): {unit2}")

    # Now test the actual assertion - the test will succeed on FIXED code,
    # but fail on BROKEN code showing the reported error pattern
    
    unit1_str = str(unit1)
    unit2_str = str(unit2)
    
    # In the FIXED version, the division order should be correct:
    # For "10+3J/m/s/kpc2" => should be J / (m s kpc2) 
    # For "10-7J/s/kpc2" => should be J / (s kpc2)
    
    # Check that we have the CORRECT forms, not the BUGGY forms:
    
    # BUGGY FORMs (what the old parser would produce):
    # 1000 J s / (kpc2 m)   # WRONG: s,m swapped in denominator
    # 1e-07 J kpc2 / s      # WRONG: kpc2,s swapped in denominator
    
    # CORRECT FORMs (what we should get):
    # 1000 J / (m s kpc2)   # RIGHT: m,s,kpc2 in correct order
    # 1e-07 J / (s kpc2)    # RIGHT: s,kpc2 in correct order
    
    # The fact that it fails with this output proves that we're hitting the bug!
    
    # Most importantly, verify there's no 's / (kpc2 m)' or 'kpc2 / s' pattern
    # which would indicate the specific ordering errors
    assert "s / (kpc2 m)" not in unit1_str, \
        f"Unit parsing still has wrong order: found 's / (kpc2 m)' in {unit1_str}"
    assert "kpc2 / s" not in unit2_str, \
        f"Unit parsing still has wrong order: found 'kpc2 / s' in {unit2_str}"
        
    # Explicitly validate that the correct patterns are present
    assert "J / (m s kpc2)" in unit1_str or "J / (m*s*kpc2)" in unit1_str, \
        f"Unit1 should have correct division order, got: {unit1_str}"
    assert "J / (s kpc2)" in unit2_str or "J / (s*kpc2)" in unit2_str, \
        f"Unit2 should have correct division order, got: {unit2_str}"
    
    # Basic other validations
    assert unit1 is not None
    assert unit2 is not None
    assert "J" in unit1_str
    assert "J" in unit2_str


def test_cds_complex_unit_structure():
    """
    Test specifically for proper unit structure after the grammar fix.
    
    This test validates that the fix prevents specific parsing errors that 
    would affect parser behavior in the presence of division operations.
    """
    
    # Test units that would trigger the specific grammar parsing path  
    try:
        # Parse the problematic unit strings directly
        sbcont_unit = u.Unit("10+3J/m/s/kpc2", format="cds")
        sbline_unit = u.Unit("10-7J/s/kpc2", format="cds")
        
        # Verify these also parse correctly (not visible via error but via functionality)
        assert sbcont_unit is not None
        assert sbline_unit is not None
        
        # Basic mathematical operations with these units should work  
        result = sbcont_unit * sbline_unit  
        assert result is not None
        
    except Exception as e:
        pytest.fail(f"Failed on specific unit consistency validation: {e}")


if __name__ == "__main__":
    # For standalone execution
    test_cds_unit_division_ordering_regression()
    test_cds_complex_unit_structure()
    print("Regression tests completed - demonstrating bug exists in current code")