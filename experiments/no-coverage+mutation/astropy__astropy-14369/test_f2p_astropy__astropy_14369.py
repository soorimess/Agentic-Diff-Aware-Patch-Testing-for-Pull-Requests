#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import pytest
from astropy.table import Table
import os
import tempfile


def test_cds_complex_unit_division_order_sbccont():
    """
    Test that SBCONT unit '10+3J/m/s/kpc2' is parsed with correct division order.
    
    The bug manifested as incorrect parsing of complex unit strings with multiple
    division operations, where the order of operands in division was reversed.
    """
    
    # Create test MRT content with the problematic SBCONT unit
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
--------------------------------------------------------------------------------
ID0001     70.99200      
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(mrt_content)
        temp_file = f.name
    
    try:
        # Read the table with CDS format  
        dat = Table.read(temp_file, format='ascii.cds')
        
        # Extract the unit
        sbcont_unit = dat['SBCONT'].unit
        
        print(f"SBCONT unit: {sbcont_unit}")
        
        # Before the fix, this would parse as: 1000 J s / (kpc2 m) [wrong order]
        # After the fix, this should parse as: 1000 J / (m s kpc2) [correct order]
        
        sbcont_str = str(sbcont_unit)
        
        # On buggy code: "s / (kpc2 m)" pattern would appear in string
        # On correct code: The ordering should be maintained as proper division
        assert "s / (kpc2 m)" not in sbcont_str, \
            f"BUG: Division order incorrect in SBCONT unit: {sbcont_str}"
            
        # The unit should have the right components in proper structural order
        assert "J" in sbcont_str
        assert "m" in sbcont_str or "m" in str(sbcont_unit)
        assert "kpc" in sbcont_str or "kpc" in str(sbcont_unit)
        assert "s" in sbcont_str or "s" in str(sbcont_unit)
        
    finally:
        os.unlink(temp_file)


def test_cds_complex_unit_division_order_sbline():
    """
    Test that SBLINE unit '10-7J/s/kpc2' is parsed with correct division order.
    
    This tests the same parsing issue with a different complex unit string.
    """
    
    # Create test MRT content with the problematic SBLINE unit
    mrt_content = """Title:
Authors:
Table:
================================================================================
Byte-by-byte Description of file: tab.txt
--------------------------------------------------------------------------------
   Bytes Format Units          		Label      Explanations
--------------------------------------------------------------------------------
   1- 10 A10    ---            		ID         ID
  12- 21 F10.5  10-7J/s/kpc2 		SBLINE     Line surface brightness
--------------------------------------------------------------------------------
ID0001     38.51040      
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(mrt_content)
        temp_file = f.name
    
    try:
        # Read the table with CDS format  
        dat = Table.read(temp_file, format='ascii.cds')
        
        # Extract the unit
        sbline_unit = dat['SBLINE'].unit
        
        print(f"SBLINE unit: {sbline_unit}")
        
        # Before the fix, this would parse as: 1e-07 J kpc2 / s [wrong order]  
        # After the fix, this should parse as: 1e-07 J / (s kpc2) [correct order]
        
        sbline_str = str(sbline_unit)
        
        # On buggy code: "kpc2 / s" pattern would appear in string
        # On correct code: The ordering should be maintained properly
        assert "kpc2 / s" not in sbline_str, \
            f"BUG: Division order incorrect in SBLINE unit: {sbline_str}"
            
        # The unit should have the right components
        assert "J" in sbline_str
        assert "s" in sbline_str or "s" in str(sbline_unit)
        assert "kpc" in sbline_str or "kpc" in str(sbline_unit)
        
    finally:
        os.unlink(temp_file)