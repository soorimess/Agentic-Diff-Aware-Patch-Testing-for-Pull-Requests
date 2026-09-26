"""
Regression test for CDS unit parsing bug in astropy.

This test ensures that composite units in MRT (CDS format) files are parsed
correctly, specifically that division operations maintain the proper order.
"""

import os
import tempfile
from astropy.table import Table


def test_cds_unit_parsing_order():
    """Test that CDS format units maintain correct order in division operations."""
    
    # Create test MRT content with problematic units
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
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(mrt_content)
        temp_filename = f.name
    
    try:
        # Read the table with CDS format
        dat = Table.read(temp_filename, format='ascii.cds')
        
        # Check the units - they should be parsed correctly
        sbcont_unit = dat['SBCONT'].unit
        sbline_unit = dat['SBLINE'].unit
        
        # The bug: SBCONT shows as "1000 J s / (kpc2 m)" instead of "1000 J / (m s kpc2)"
        # The issue is that in the denominator, the order is wrong:
        # kpc2 m instead of m kpc2 (and s is in the numerator instead of denominator)
        
        sbcont_str = str(sbcont_unit)
        sbline_str = str(sbline_unit)
        
        # The key assertion: the buggy version has "s / (kpc2 m)" 
        # which means s is in the numerator and kpc2, m are in denominator in wrong order
        # The correct version should have "J / (m s kpc2)" - all in denominator in correct order
        
        # Test that we don't have the buggy pattern
        assert 's / (kpc2 m)' not in sbcont_str, (
            f"BUG DETECTED: SBCONT has incorrect unit order. "
            f"Got: {sbcont_str}. This shows s in numerator instead of denominator."
        )
        
        # Also test that SBLINE doesn't have the same issue
        assert 'kpc2 / s' not in sbline_str, (
            f"BUG DETECTED: SBLINE has incorrect unit order. "
            f"Got: {sbline_str}. This shows kpc2 in numerator instead of denominator."
        )
        
        # The correct behavior should be that all units are in the denominator in proper order
        # For SBCONT: 10+3J/m/s/kpc2 should be parsed as 1000 J / (m * s * kpc2)
        # For SBLINE: 10-7J/s/kpc2 should be parsed as 1e-7 J / (s * kpc2)
        
    finally:
        # Clean up temp file
        os.unlink(temp_filename)