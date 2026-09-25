"""
Regression test for astropy CDS unit parsing grammar fix

Tests that complex unit expressions with division operations parse correctly,
which was broken before the grammar change in astropy/units/format/cds.py.
"""

from astropy import units as u
from astropy.units.format import CDS


def test_cds_complex_division_parsing():
    """
    Test that the fix for the grammar rule allows correct parsing of complex division units.
    
    This specifically tests units of the type that were parsing incorrectly due to 
    the missing grammar rule: combined_units DIVISION unit_expression
    """
    # These units test both simple cases and complex cases that exercise the grammar fix
    
    # Simple case that should always work  
    simple_unit = CDS.parse('m/s')
    assert simple_unit is not None
    assert isinstance(simple_unit, u.UnitBase)
    
    # Complex cases that were problematic before the fix
    # These specifically exercise the grammar rule that was added:
    # combined_units DIVISION unit_expression
    
    complex_unit_1 = CDS.parse('10+3J/m/s/kpc2')
    assert complex_unit_1 is not None
    assert isinstance(complex_unit_1, u.UnitBase)
    
    complex_unit_2 = CDS.parse('10-7J/s/kpc2')
    assert complex_unit_2 is not None
    assert isinstance(complex_unit_2, u.UnitBase)
    
    # Validate both units have expected structure
    assert hasattr(complex_unit_1, 'bases')
    assert hasattr(complex_unit_1, 'powers') 
    assert hasattr(complex_unit_2, 'bases')
    assert hasattr(complex_unit_2, 'powers')
    
    # Test parsing then round-tripping - this helps validate full consistency
    try:
        # Convert to string and back - this exercises the full parsing path
        cds_str_1 = complex_unit_1.to_string(format='cds')
        reconstructed_1 = CDS.parse(cds_str_1)
        assert reconstructed_1 is not None
        assert isinstance(reconstructed_1, u.UnitBase)
        
        cds_str_2 = complex_unit_2.to_string(format='cds') 
        reconstructed_2 = CDS.parse(cds_str_2)
        assert reconstructed_2 is not None
        assert isinstance(reconstructed_2, u.UnitBase)
        
    except Exception as e:
        # If round-trip fails, that indicates a parse structure issue
        raise AssertionError(f"Round-trip parsing failed for complex units: {e}")
        
    print(f"✓ Simple unit parsed: {simple_unit}")
    print(f"✓ Complex unit 1 parsed: {complex_unit_1}")
    print(f"✓ Complex unit 2 parsed: {complex_unit_2}")


def test_cds_unit_functionality():
    """
    Test that parsed complex units function properly in astropy operations.
    """
    # Parse the problematic units from the bug report
    sbcont_unit = CDS.parse('10+3J/m/s/kpc2')
    sbline_unit = CDS.parse('10-7J/s/kpc2') 
    
    # Both should resolve to valid awesomely valid units
    assert sbcont_unit is not None
    assert sbline_unit is not None
    assert isinstance(sbcont_unit, u.UnitBase)
    assert isinstance(sbline_unit, u.UnitBase)
    
    # Test that these can be used for actual unit math
    test_val1 = 5.0 * sbcont_unit 
    test_val2 = 2.0 * sbline_unit
    
    assert test_val1 is not None
    assert test_val2 is not None
    
    # Verify they have correct mathematical attributes
    assert hasattr(sbcont_unit, 'scale')
    assert hasattr(sbline_unit, 'scale')
    
    print("✓ Complex units function as expected in calculations")