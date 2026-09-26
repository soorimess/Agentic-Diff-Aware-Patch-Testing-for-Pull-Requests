# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression test for CDS unit parsing bug.

This test specifically checks that CDS units with division operations
are parsed with the correct mathematical structure.
"""

from astropy.units.format.cds import CDS


def test_cds_unit_mathematical_structure():
    """
    Test that CDS units preserve correct mathematical structure.
    
    The bug was in the grammar rule for division_of_units which changed from:
    | unit_expression DIVISION combined_units
    to:
    | combined_units DIVISION unit_expression
    
    This caused division operations to be parsed with wrong mathematical meaning.
    
    For the unit "10+3J/m/s/kpc2", the correct mathematical structure should be:
    - J with power 1 (numerator)
    - m with power -1 (denominator) 
    - s with power -1 (denominator)
    - kpc with power -2 (denominator)
    
    This means the unit should be: J / (m * s * kpc^2) = J * m^-1 * s^-1 * kpc^-2
    
    The bug caused it to be parsed as: J * s * kpc^-2 * m^-1 = J * s / (kpc^2 * m)
    where s was incorrectly treated as a numerator instead of denominator.
    """
    
    # Parse the problematic unit from the bug report
    unit = CDS.parse("10+3J/m/s/kpc2")
    
    # Check that parsing succeeds
    assert unit is not None
    
    # Check the mathematical structure by examining bases and powers
    # For correct parsing: J^1 * m^-1 * s^-1 * kpc^-2
    bases = unit.bases
    powers = unit.powers
    
    # Convert bases to strings for easier comparison
    base_names = [str(base) for base in bases]
    
    # The unit should contain these bases in this order
    expected_bases = ['J', 'm', 's', 'kpc']
    expected_powers = [1, -1, -1, -2]  # J^1 * m^-1 * s^-1 * kpc^-2
    
    # Check that we have the right number of units
    assert len(bases) == 4, f"Expected 4 bases, got {len(bases)}"
    assert len(powers) == 4, f"Expected 4 powers, got {len(powers)}"
    
    # Check that the bases are correct
    assert base_names == expected_bases, f"Expected bases {expected_bases}, got {base_names}"
    
    # The key test: check that powers are correct
    # If the bug is present, s will have power 1 instead of -1
    assert powers == expected_powers, f"Expected powers {expected_powers}, got {powers}"
    
    # Test that we can create quantities with this unit
    try:
        quantity = 5.0 * unit
        assert quantity is not None
    except Exception as e:
        raise AssertionError(f"Failed to create quantity with unit: {e}")
    
    # Test that the unit can be used in calculations
    try:
        # Test that we can convert to string without error
        unit_str = CDS.to_string(unit)
        assert unit_str is not None
    except Exception as e:
        raise AssertionError(f"Failed to convert unit to string: {e}")
        
    # Test a few more cases to make sure the parsing is generally correct
    test_cases = [
        ("m/s", ["m", "s"], [1, -1]),
        ("10+3J/m/s/kpc2", ["J", "m", "s", "kpc"], [1, -1, -1, -2]),
        ("10-7J/s/kpc2", ["J", "s", "kpc"], [1, -1, -2])
    ]
    
    for unit_str, expected_bases, expected_powers in test_cases:
        parsed = CDS.parse(unit_str)
        assert parsed is not None, f"Failed to parse {unit_str}"
        
        # For simple cases, we can check the structure
        if len(expected_bases) <= 2:  # Only check simple cases
            bases = [str(b) for b in parsed.bases]
            powers = parsed.powers
            assert bases == expected_bases, f"For {unit_str}: expected bases {expected_bases}, got {bases}"
            assert powers == expected_powers, f"For {unit_str}: expected powers {expected_powers}, got {powers}"


def test_cds_unit_parsing_basic():
    """
    Basic test that CDS unit parsing works without errors.
    """
    # These should all parse without raising exceptions
    test_units = [
        "m/s",
        "kg", 
        "J",
        "10+3J/m/s/kpc2",
        "10-7J/s/kpc2"
    ]
    
    for unit_str in test_units:
        parsed = CDS.parse(unit_str)
        assert parsed is not None, f"Failed to parse unit: {unit_str}"
        
        # Test round-trip
        try:
            roundtrip = CDS.to_string(parsed)
            assert roundtrip is not None
        except Exception as e:
            raise AssertionError(f"Failed to round-trip unit {unit_str}: {e}")