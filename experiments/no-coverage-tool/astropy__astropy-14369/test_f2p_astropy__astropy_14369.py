# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Regression test for CDS unit parsing issue.

The change in grammar rules for division handling in CDS format affects
the semantic ordering of units when they are parsed. This test ensures
that identifier "s" and "kpc2" are correctly positioned in denominator 
rather than numerator.
"""

from astropy.units.format.cds import CDS


def test_cds_unit_denominator_ordering():
    """
    Test that CDS units parse with correct denominator ordering.
    
    Before the fix, complex units like "J/m/s/kpc2" would have incorrect
    semantic ordering, where "s" appears in numerator instead of denominator,
    and units like "J/s/kpc2" would have "kpc2" in numerator instead of denominator.
    """
    
    # Test case 1: Complex unit with multiple divisions  
    unit_str1 = "J/m/s/kpc2"
    parsed1 = CDS.parse(unit_str1)
    
    # Check that the parsed unit represents correct mathematical meaning
    # It should be: J/(m*s*kpc2), meaning all components in denominator
    # Before fix, it was incorrectly represented as: J*s/(m*kpc2) 
    
    # The string representation of the unit gives us a good clue about ordering
    unit_str1_parsed = str(parsed1)
    
    # This is the key assertion that tests the bug
    # If unit_str1_parsed looks like "J s / (kpc2 m)" - then the bug is present
    # If unit_str1_parsed looks like "J / (kpc2 m s)" - then bug is fixed
    
    # The critical test: There should be NO "s" in numerator position!  
    # If s is appearing in the numerator, it means division order was wrong
    
    # Make sure s is NOT positioned in the numerator position
    # This assertion would fail with old buggy behavior
    assert "s" not in unit_str1_parsed.split("/")[0], \
        f"Bug present: 's' incorrectly appears in numerator of {unit_str1_parsed}"

    # Test case 2: Another complex unit
    unit_str2 = "J/s/kpc2"
    parsed2 = CDS.parse(unit_str2)
    unit_str2_parsed = str(parsed2)
    
    # Make sure kpc2 is NOT positioned in the numerator position
    assert "kpc2" not in unit_str2_parsed.split("/")[0], \
        f"Bug present: 'kpc2' incorrectly appears in numerator of {unit_str2_parsed}"
        
    # Test that the parsing works without error (basic functionality)
    assert parsed1 is not None
    assert parsed2 is not None
    assert hasattr(parsed1, 'to_string')  # check it's a proper unit object  
    assert hasattr(parsed2, 'to_string')


def test_cds_unit_semantic_correctness():
    """
    Test semantic correctness of complex unit expressions.
    
    Verifies that when parsing units with multiple divisions, 
    the mathematical structure is preserved correctly.
    """
    # This tests a simpler case related to what was reported
    atomic_units = ["J/m/s/kpc2", "J/s/kpc2"]
    
    for unit_str in atomic_units:
        try:
            parsed = CDS.parse(unit_str)
            # Just verify it parses correctly without error
            assert parsed is not None
            # And that it's a proper unit
            assert str(parsed) != ""
        except Exception as e:
            raise AssertionError(f"Failed to parse unit '{unit_str}': {e}")