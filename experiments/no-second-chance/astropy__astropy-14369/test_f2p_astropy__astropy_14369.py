"""Test for regression of CDS units parsing bug in astropy.

This test pins down the specific bug where complex CDS units like 
'10+3J/m/s/kpc2' and '10-7J/s/kpc2' are parsed with incorrect division ordering.

The bug was in the grammar rule in astropy/units/format/cds.py that changed
the parsing of division operations from:
    DIVISION unit_expression 
    | unit_expression DIVISION combined_units
to:
    DIVISION unit_expression
    | combined_units DIVISION unit_expression
"""
from astropy.units.format import CDS


def test_cds_complex_unit_division_order_regression():
    """
    Regression test for CDS unit parsing bug where division order was reversed.
    
    The issue was that when parsing complex CDS units like '10+3J/m/s/kpc2',
    the division components were incorrectly ordered in the resulting unit.
    
    Before fix, this would parse as '1000 J s / (kpc2 m)' instead of '1000 J / (m s kpc2)'.
    """
    # Test case 1: The SBCONT unit that was reported as problematic
    sbcont_unit_text = "10+3J/m/s/kpc2"  # Should be 1000 J / (m s kpc2)
    parsed_sbcont = CDS.parse(sbcont_unit_text)  
    sbcont_str = str(parsed_sbcont)
    
    # The specific bug symptom was that units were returned in wrong order
    # Check that we're NOT seeing the wrong order of components  
    # The buggy parsing yielded: 1000 J s / (kpc2 m) - wrong order in denominator
    # The correct parsing should yield: 1000 J / (m s kpc2) - proper order
    assert '1000 J s / (kpc2 m)' != sbcont_str, (
        f"Regression: Division order bug still present in SBCONT unit. "
        f"Got '{sbcont_str}' - this shows incorrect component ordering in denominator."
    )
    
    # Test case 2: The SBLINE unit that was also reported as problematic
    sbline_unit_text = "10-7J/s/kpc2"  # Should be 1e-7 J / (s kpc2)  
    parsed_sbline = CDS.parse(sbline_unit_text)
    sbline_str = str(parsed_sbline)
    
    # The bug was that this would show as: 1e-07 J kpc2 / s (kpc2 before s)
    # But should be: 1e-07 J / (s kpc2) 
    assert '1e-07 J kpc2 / s' != sbline_str, (
        f"Regression: Division order bug still present in SBLINE unit. "
        f"Got '{sbline_str}' - this shows incorrect component ordering in denominator."
    )


def test_cds_unit_parsing_still_works():
    """Test that unit parsing continues to work without crashing."""
    # Basic test to ensure we didn't break the parsing system completely
    
    # This should parse without error  
    unit_text = "10+3J/m/s/kpc2"
    parsed_unit = CDS.parse(unit_text)
    
    # We should be able to work with the resulting unit
    assert parsed_unit is not None
    assert hasattr(parsed_unit, 'to_string')
    
    # Check basic unit properties still work
    assert 'J' in str(parsed_unit) or 'joule' in str(parsed_unit).lower()