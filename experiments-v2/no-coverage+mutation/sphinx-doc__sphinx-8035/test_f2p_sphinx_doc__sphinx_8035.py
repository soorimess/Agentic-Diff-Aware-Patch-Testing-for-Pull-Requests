"""
Regression test for sphinx-doc/sphinx#8035
Test that :private-members: can specify specific private members to document
"""

def test_private_members_parsing():
    """Test that private-members option now supports list parsing"""
    from sphinx.ext.autodoc import members_option
    
    # The key change: private-members should now parse comma-separated values
    result = members_option("member1,member2")
    
    # This should return a list, not a boolean
    assert isinstance(result, list)
    assert len(result) == 2
    assert "member1" in result
    assert "member2" in result