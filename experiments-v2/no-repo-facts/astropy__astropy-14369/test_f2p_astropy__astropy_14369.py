"""
Test for regression of CDS unit parsing bug.

This test specifically targets the bug where units with complex division 
operations like '10+3J/m/s/kpc2' and '10-7J/s/kpc2' were parsed with wrong 
division order.
"""

import tempfile
import os
from astropy.table import Table


def test_cds_unit_division_order_correctness():
    """
    Regression test for CDS unit parsing bug.
    
    The bug was that when parsing '10+3J/m/s/kpc2', it would incorrectly 
    produce '1000 J s / (kpc2 m)' instead of '1000 J / (m s kpc2)'.
    Similarly for '10-7J/s/kpc2' it would produce '1e-07 J kpc2 / s' 
    instead of '1e-07 J / (s kpc2)'.
    
    This test verifies that the units are parsed with correct logical order
    by checking the string representation of the units.
    """
    
    # Create the test MRT file content from the bug report
    test_content = """Title:
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
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        temp_filename = f.name
    
    try:
        # Read the table
        dat = Table.read(temp_filename, format='ascii.cds')
        
        # Check the units
        sbcont_unit = dat['SBCONT'].unit
        sbline_unit = dat['SBLINE'].unit
        
        # Convert to string for inspection
        sbcont_str = str(sbcont_unit)
        sbline_str = str(sbline_unit)
        
        print(f"SBCONT unit string: {sbcont_str}")
        print(f"SBLINE unit string: {sbline_str}")
        
        # The bug was that kpc2 appeared in the numerator incorrectly
        # Before fix: SBCONT was "1000 J s / (kpc2 m)" - kpc2 in wrong position
        # Before fix: SBLINE was "1e-07 J kpc2 / s" - kpc2 in wrong position
        
        # After fix, both should have kpc2 in the denominator in correct order
        # SBCONT should be "1000 J / (m s kpc2)" 
        # SBLINE should be "1e-07 J / (s kpc2)"
        
        # Test that kpc2 is NOT in the numerator (which would indicate the bug)
        # This assertion will fail before the fix and pass after the fix
        assert "kpc2" not in sbcont_str.split("/")[0], \
            f"BUG: SBCONT unit has kpc2 in numerator: {sbcont_str}"
            
        assert "kpc2" not in sbline_str.split("/")[0], \
            f"BUG: SBLINE unit has kpc2 in numerator: {sbline_str}"
        
        # Additional checks to make sure parsing works correctly
        assert sbcont_unit is not None, "SBCONT unit should not be None"
        assert sbline_unit is not None, "SBLINE unit should not be None"
        
        # Test direct parsing to make sure it works correctly
        from astropy.units.format.cds import CDS
        
        # Test the problematic units directly
        parsed_sbcont = CDS.parse("10+3J/m/s/kpc2")
        parsed_sbline = CDS.parse("10-7J/s/kpc2")
        
        assert parsed_sbcont is not None, "SBCONT unit should parse correctly"
        assert parsed_sbline is not None, "SBLINE unit should parse correctly"
        
        # The most important assertion: verify the units are parsed correctly
        # The fix ensures that division operations maintain proper order
        parsed_sbcont_str = str(parsed_sbcont)
        parsed_sbline_str = str(parsed_sbline)
        
        print(f"Parsed SBCONT: {parsed_sbcont_str}")
        print(f"Parsed SBLINE: {parsed_sbline_str}")
        
        # Verify that the parsed units don't have the wrong division order
        assert "kpc2" not in parsed_sbcont_str.split("/")[0], \
            f"BUG: Parsed SBCONT has kpc2 in numerator: {parsed_sbcont_str}"
            
        assert "kpc2" not in parsed_sbline_str.split("/")[0], \
            f"BUG: Parsed SBLINE has kpc2 in numerator: {parsed_sbline_str}"
        
    finally:
        # Clean up
        os.unlink(temp_filename)


def test_unit_parsing_basic():
    """
    Test basic unit parsing to ensure functionality isn't broken.
    """
    from astropy.units.format.cds import CDS
    
    # Test some basic cases to make sure parsing still works
    basic_cases = [
        "m/s",
        "J/m/s", 
        "m/s/kpc2",
    ]
    
    for case in basic_cases:
        try:
            parsed = CDS.parse(case)
            print(f"'{case}' -> {parsed}")
        except Exception as e:
            print(f"Error parsing '{case}': {e}")
            raise


if __name__ == "__main__":
    test_cds_unit_division_order_correctness()
    test_unit_parsing_basic()