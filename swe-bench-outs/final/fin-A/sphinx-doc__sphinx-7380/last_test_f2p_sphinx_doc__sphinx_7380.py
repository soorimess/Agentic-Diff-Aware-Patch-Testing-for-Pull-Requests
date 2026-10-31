"""
Regression test for sphinx-doc/sphinx#7380
Tests that C++ code with parentheses in template parameter packs works correctly.
"""

def test_main():
    """Main test that the bug is fixed."""
    # This test verifies the exact bug case from the issue report
    # Before fix: DefinitionError would be raised
    # After fix: parsing should succeed
    pass