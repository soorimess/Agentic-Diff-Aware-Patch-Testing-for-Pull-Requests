"""
Regression test for astropy issue with CDS unit parsing.

This test verifies that units from MRT (CDS format) files are parsed correctly
and that the order of division operations is preserved.
"""

from astropy.table import Table
from astropy.units import format as uformat


def test_cds_unit_division_order_regression():
    """
    Regression test for CDS unit parsing bug where division order was incorrect.
    
    The bug was that units like "10+3J/m/s/kpc2" were parsed with wrong division order,
    specifically the order of units in the denominator was reversed.
    
    Before fix: "10+3J/m/s/kpc2" parsed as "1000 J s / (kpc2 m)" (wrong order)
    After fix:  "10+3J/m/s/kpc2" parsed as "1000 J / (kpc2 m s)" (correct order)
    """
    
    # Test the specific problematic case from the bug report
    unit_complex = "10+3J/m/s/kpc2"
    parsed_complex = uformat.CDS.parse(unit_complex)
    
    # The test verifies that we don't have the buggy behavior
    # The buggy behavior was having s before m in the denominator
    unit_str = str(parsed_complex)
    assert "s / (kpc2 m)" not in unit_str, \
        "Unit should not have buggy division order (s before m in denominator)"
    
    # Test with table reading as in the original bug report
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
    
    # Write test file
    with open('test_tab.txt', 'w') as f:
        f.write(mrt_content)
    
    # Read the table
    dat = Table.read('test_tab.txt', format='ascii.cds')
    
    # Check that the units are parsed correctly
    sbcont_unit = dat['SBCONT'].unit
    sbline_unit = dat['SBLINE'].unit
    
    # Verify that we don't have the buggy behavior that was reported in the issue
    sbcont_str = str(sbcont_unit)
    sbline_str = str(sbline_unit)
    
    # The bug showed SBCONT as "1e+3 J s / (kpc2 m)" - wrong order
    assert "s / (kpc2 m)" not in sbcont_str, \
        "SBCONT should not have wrong division order (s before m in denominator)"
    
    # The bug showed SBLINE as "1e-7 J kpc2 / s" - wrong order  
    assert "kpc2 / s" not in sbline_str, \
        "SBLINE should not have wrong division order (kpc2 before s in denominator)"