# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""Regression tests for CDS unit parsing bug."""

import os
import tempfile

from astropy.table import Table


def test_cds_unit_denominator_order():
    """Test that composite units from CDS format have correct denominator order.
    
    This test verifies that units like '10+3J/m/s/kpc2' are parsed with 
    correct relative ordering of units in the denominator.
    
    The bug shows that the units in the denominator are in the wrong order,
    e.g., '1000 J s / (kpc2 m)' instead of '1000 J / (m s kpc2)'.
    """
    # Create a temporary MRT file with the problematic units from the bug report
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
        # Read with CDS format 
        dat = Table.read(temp_filename, format='ascii.cds')
        
        # Get the string representations of the units - this is what's actually parsed
        sbcont_str = str(dat['SBCONT'].unit)
        sbline_str = str(dat['SBLINE'].unit)
        
        # The bug causes wrong ordering in denominator
        # Before the fix: '1000 J s / (kpc2 m)'  - wrong order (s,m instead of m,s)
        # After the fix: '1000 J / (m s kpc2)'   - correct order
        
        # Test for the symptom - if we see kpc2 m in the denominator, that's the bug
        assert 'kpc2 m' not in sbcont_str, (
            f"Bug present: SBCONT unit has wrong denominator order: {sbcont_str}. "
            f"Should be '1000 J / (m s kpc2)'"
        )
        
        # Similarly, for SBLINE: 
        # Before the fix: '1e-07 J kpc2 / s' - wrong order (kpc2,s instead of s,kpc2)
        # After the fix: '1e-07 J / (s kpc2)' - correct order
        assert 'kpc2 s' not in sbline_str, (
            f"Bug present: SBLINE unit has wrong denominator order: {sbline_str}. "
            f"Should be '1e-07 J / (s kpc2)'"
        )
        
        # If we get here, the units are correct - no bug present
        # We should be able to see correct unit ordering
        assert 'm s kpc2' in sbcont_str or 'm*s*kpc2' in sbcont_str, (
            f"SBCONT unit should have correct denominator order: {sbcont_str}"
        )
        assert 's kpc2' in sbline_str or 's*kpc2' in sbline_str, (
            f"SBLINE unit should have correct denominator order: {sbline_str}"
        )
        
    finally:
        # Clean up temp file
        os.unlink(temp_filename)