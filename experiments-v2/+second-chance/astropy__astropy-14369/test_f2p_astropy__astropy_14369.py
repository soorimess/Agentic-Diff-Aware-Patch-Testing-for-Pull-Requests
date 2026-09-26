# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression test for astropy issue with CDS unit parsing.
"""

def test_cds_unit_division_order():
    """
    Regression test for CDS unit parsing bug.
    
    This test verifies that units like 'J/m/s/kpc2' are parsed with correct 
    division order, not the incorrect 'J s / (kpc2 m)' that was reported in the bug.
    """
    from astropy.units.format.cds import CDS
    
    # Parse a unit that was problematic in the bug report
    unit_str = "J/m/s/kpc2"
    parsed_unit = CDS.parse(unit_str)
    
    # Convert to string to check the representation
    unit_str_result = str(parsed_unit)
    
    # The test verifies that we don't get the incorrect order pattern
    # that was reported in the bug (J s / (kpc2 m) instead of J / (m s kpc2))
    assert "kpc2 m" not in unit_str_result, (
        f"Bug still present: got incorrect order '{unit_str_result}'"
    )