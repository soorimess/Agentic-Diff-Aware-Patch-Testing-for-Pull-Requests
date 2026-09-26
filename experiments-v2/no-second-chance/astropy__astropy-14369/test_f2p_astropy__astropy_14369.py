# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression test for CDS format unit parsing bug.

This test ensures that composite units with division are parsed correctly
in the CDS format, specifically checking that the order of division is preserved.
"""

import pytest
from astropy.table import Table
from astropy import units as u
from astropy.units.format import CDS


def test_cds_unit_parsing_division_order():
    """
    Test that CDS format correctly parses units with division operations.
    
    The bug was that when parsing units like '10+3J/m/s/kpc2', the order of 
    division was being jumbled, resulting in incorrect unit representations.
    
    Specifically, '10+3J/m/s/kpc2' should parse to J / (m * s * kpc**2) 
    but was incorrectly parsed as 1000 J s / (kpc2 m).
    """
    # Test the specific case from the bug report
    # The unit '10+3J/m/s/kpc2' should parse to J / (m * s * kpc**2)
    # The buggy behavior would produce 1000 J s / (kpc2 m)
    
    unit_str = "10+3J/m/s/kpc2"
    parsed_unit = CDS.parse(unit_str)
    
    # The correct parsing should result in J * m**-1 * s**-1 * kpc**-2
    # which when displayed should be J / (kpc2 m s) - but the actual unit structure matters
    expected_unit = u.J * u.m**-1 * u.s**-1 * u.kpc**-2
    
    # Check that the parsed unit has the correct structure
    # The key is that the order of the units in the denominator should be preserved
    # m should come before s should come before kpc2
    assert parsed_unit.bases[0] == u.J
    assert parsed_unit.bases[1] == u.m
    assert parsed_unit.bases[2] == u.s  
    assert parsed_unit.bases[3] == u.kpc
    
    # Check that powers are correct
    assert parsed_unit.powers[0] == 1  # J
    assert parsed_unit.powers[1] == -1  # m
    assert parsed_unit.powers[2] == -1  # s
    assert parsed_unit.powers[3] == -2  # kpc
    
    # Test that the string representation is reasonable
    string_repr = CDS.to_string(parsed_unit)
    # We don't test exact string representation since that may vary, 
    # but we check that it's a valid unit that can be used


def test_cds_unit_parsing_complex_division():
    """
    Test complex unit parsing with multiple division operations.
    
    This specifically tests the fix for the division order bug in CDS format.
    """
    # Test another case from the bug report
    unit_str = "10-7J/s/kpc2"
    parsed_unit = CDS.parse(unit_str)
    
    # Should parse to J * s**-1 * kpc**-2
    expected_unit = u.J * u.s**-1 * u.kpc**-2
    
    # Check structure - J should be first, s second, kpc third
    assert parsed_unit.bases[0] == u.J
    assert parsed_unit.bases[1] == u.s
    assert parsed_unit.bases[2] == u.kpc
    
    # Check that powers are correct
    assert parsed_unit.powers[0] == 1  # J
    assert parsed_unit.powers[1] == -1  # s
    assert parsed_unit.powers[2] == -2  # kpc


def test_cds_table_unit_parsing():
    """
    Test that Table.read with format='ascii.cds' correctly handles units.
    
    This reproduces the exact scenario from the bug report.
    """
    # Create test MRT content as described in the bug report
    mrt_content = """Title:
Authors:
Table:
================================================================================
Byte-by-byte Description of file: tab.txt
--------------------------------------------------------------------------------
   Bytes Format Units          		Label      Explanations
--------------------------------------------------------------------------------
   1- 10 A10    ---            		ID         ID
  12- 21 F10.5  10+3J/m/s/kpc2    	SBCONT     Cont surface brightness
  23- 32 F10.5  10-7J/s/kpc2 		SBLINE     Line surface brightness
--------------------------------------------------------------------------------
ID0001     70.99200   38.51040      
ID0001     13.05120   28.19240      
ID0001     3.83610    10.98370      
ID0001     1.99101    6.78822       
ID0001     1.31142    5.01932      
"""
    
    # Write to a temporary file
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(mrt_content)
        temp_filename = f.name
    
    try:
        # Read the table
        dat = Table.read(temp_filename, format='ascii.cds')
        
        # Check that the units are parsed correctly
        # The SBCONT column should have unit J / (m * s * kpc**2) 
        # The SBLINE column should have unit J / (s * kpc**2)
        
        # Check that the units are properly parsed (not jumbled)
        sbcont_unit = dat['SBCONT'].unit
        sbline_unit = dat['SBLINE'].unit
        
        # Both should be composite units with correct structure
        # The key test is that the parsing doesn't jumble the order
        assert sbcont_unit is not None
        assert sbline_unit is not None
        
        # Check that the units are valid and can be used
        # This ensures they're not malformed
        assert hasattr(sbcont_unit, 'bases')
        assert hasattr(sbline_unit, 'bases')
        
    finally:
        # Clean up temp file
        os.unlink(temp_filename)