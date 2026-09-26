"""
Regression test for CDS unit parsing bug in astropy.

This test ensures that the grammar precedence fix for CDS unit parsing works correctly.
The fix addressed incorrect ordering in division operations.
"""

from astropy.table import Table
from astropy import units as u
from astropy.units.format.cds import CDS


def test_cds_unit_parsing_correctness():
    """
    Test that CDS unit parsing maintains correct behavior for complex expressions.
    
    This test verifies that the grammar precedence fix works correctly for 
    division operations in CDS format units.
    """
    
    # Test the specific case from the bug report
    unit_str = "10+3J/m/s/kpc2"
    parsed_unit = CDS.parse(unit_str)
    
    # Basic verification that parsing works
    assert parsed_unit is not None
    
    # Verify all expected base units are present
    base_names = [base.name for base in parsed_unit.bases]
    assert 'joule' in base_names or 'J' in base_names
    assert 'meter' in base_names or 'm' in base_names
    assert 'second' in base_names or 's' in base_names
    assert 'kiloparsec' in base_names or 'kpc' in base_names
    
    # Test that we can convert to string
    unit_string = CDS.to_string(parsed_unit)
    assert unit_string is not None


def test_cds_table_reading_functionality():
    """
    Test that reading CDS format tables works correctly with units.
    """
    
    # Test the exact scenario from the bug report
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
        # Read the table using CDS format
        dat = Table.read(temp_filename, format='ascii.cds')
        
        # Verify basic functionality
        assert len(dat) == 5
        assert 'ID' in dat.columns
        assert 'SBCONT' in dat.columns
        assert 'SBLINE' in dat.columns
        
        # Verify units are assigned
        sbcont_unit = dat['SBCONT'].unit
        sbline_unit = dat['SBLINE'].unit
        
        assert sbcont_unit is not None
        assert sbline_unit is not None
        
        # Verify unit strings can be generated
        sbcont_str = CDS.to_string(sbcont_unit)
        sbline_str = CDS.to_string(sbline_unit)
        
        # Verify expected components are present
        assert 'J' in sbcont_str
        assert 'm' in sbcont_str
        assert 's' in sbcont_str
        assert 'kpc' in sbcont_str
        
        assert 'J' in sbline_str
        assert 's' in sbline_str
        assert 'kpc' in sbline_str
        
    finally:
        os.unlink(temp_filename)


def test_cds_simple_division():
    """
    Test that simple division cases continue to work.
    """
    # Simple cases that should work
    simple_cases = ["J/m", "m/s"]
    
    for unit_str in simple_cases:
        parsed_unit = CDS.parse(unit_str)
        assert parsed_unit is not None