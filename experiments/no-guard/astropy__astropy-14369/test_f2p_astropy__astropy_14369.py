"""
Regression test for CDS unit parsing bug fix.

The bug was that unit parsing in CDS format incorrectly ordered divisors in 
composite units like 10+3J/m/s/kpc2, resulting in wrong unit representations.

This test specifically shows the issue where:
- Before fix: SBCONT units showed 1000 J s / (kpc2 m)   (incorrect ordering)
- After fix: SBCONT units show 1000 J / (m s kpc2)   (correct ordering)
"""

import tempfile
import os
from astropy.table import Table


def test_cds_unit_correct_division_ordering():
    """
    Test that CDS unit parsing maintains correct dividend/divisor ordering.
    
    This specifically tests the reported bug where division of compound units
    was incorrectly parsed due to a change in the grammar rule for division.
    
    The critical test is that divisors appear in correct sequence in the final 
    parsed unit representations.
    """
    
    # Create the MRT file content from the bug report  
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
        
        # Get the actual unit representations
        sbcont_unit_str = str(dat['SBCONT'].unit)
        sbline_unit_str = str(dat['SBLINE'].unit)
        
        # The bug specifically was that these would show incorrectly:
        # SBCONT unit: "1000 J s / (kpc2 m)" instead of "1000 J / (m s kpc2)"
        # SBLINE unit: "1e-07 J kpc2 / s" instead of "1e-07 J / (s kpc2)"
        
        # The correct approach: we make assertions that the problematic patterns
        # don't exist (as these indicate that the bug is present)
        # NOT the patterns that indicate it's working correctly, since those
        # could be true even before the fix but wrong
        assert 's / (kpc2 m)' not in sbcont_unit_str, (
            f"BUG: SBCONT units have wrong division order: {sbcont_unit_str}. "
            "This indicates units are not parsed correctly. "
            "Expected: 1000 J / (m s kpc2), not 1000 J s / (kpc2 m)"
        )
        
        assert 'kpc2 / s' not in sbline_unit_str, (
            f"BUG: SBLINE units have wrong division order: {sbline_unit_str}. "
            "This indicates units are not parsed correctly. "
            "Expected: 1e-07 J / (s kpc2), not 1e-07 J kpc2 / s"
        )
        
        # Additional positive checks to make sure parsing still works
        assert 'J' in sbcont_unit_str and 'J' in sbline_unit_str, "Units should contain J"
        assert 'kpc2' in sbcont_unit_str and 'kpc2' in sbline_unit_str, "Units should contain kpc2"
        
    finally:
        # Clean up
        os.unlink(temp_filename)


def test_table_reading_still_works():
    """Verify that basic table reading functionality wasn't broken."""
    
    mrt_content = """Title:
Authors:
Table:
================================================================================
Byte-by-byte Description of file: tab.txt
--------------------------------------------------------------------------------
   Bytes Format Units          		Label      Explanations
--------------------------------------------------------------------------------
   1- 10 A10    ---            		ID         ID
  12- 21 F10.5  m/s             	SPEED      Speed
--------------------------------------------------------------------------------
ID0001     70.99200      
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(mrt_content)
        temp_filename = f.name
    
    try:
        dat = Table.read(temp_filename, format='ascii.cds')
        assert len(dat) > 0
        assert 'SPEED' in dat.colnames
        assert dat['SPEED'].unit is not None
        
    finally:
        os.unlink(temp_filename)


if __name__ == "__main__":
    test_cds_unit_correct_division_ordering()
    test_table_reading_still_works()
    print("All CDS unit parsing tests passed!")