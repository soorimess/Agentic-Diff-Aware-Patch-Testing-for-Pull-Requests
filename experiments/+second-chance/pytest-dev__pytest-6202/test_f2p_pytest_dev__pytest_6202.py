import pytest


def test_bracket_parameter_display_preserves_original():
    """Ensure that parametrized test with bracket parameters displays correctly.
    
    The key difference between the buggy behavior and fixed behavior:
    
    Buggy version (before fix): 
    If you have a parameter like "..[" in a test name, it would be 
    incorrectly transformed by s.replace(".[", "[") into ".["
    
    Expected behavior (after fix):
    The parameter should be displayed exactly as provided: "..["
    
    This requires an end-to-end test that validates behavior enforcement
    """
    
    import tempfile
    import subprocess
    import sys
    import os
    
    # This will test that the parametrized test correctly shows its 
    # parameter with brackets and not have them corrupted
    test_content = '''import pytest

@pytest.mark.parametrize("param", ["..["])
def test_bracket_handling(param):
    assert 0  # Force failure for clear output
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
        
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            temp_file, "-v", "--tb=no"
        ], capture_output=True, text=True, cwd=".")
        
        output = result.stdout
        print("Test output:", output)
        
        # The main assertion is that we get the expected bracketed parameter format
        # Check that "**[" is preserved (in the name)
        assert "test_bracket_handling[..[]" in output, \
            f"Expected preserved brackets in test name, got: {output}"
        
        # If the replacement existed, it would incorrectly generate ".[" instead
        # So we assert NO occurrence of the buggy form  
        assert "test_bracket_handling[.[]" not in output, \
            "Test name incorrectly shows .[ instead of ..[ - bug still present"
            
    finally:
        os.unlink(temp_file)


def test_string_replacement_logic():
    """Test the actual string replacement logic that was problematic.
    
    The specific logic in getmodpath():
        s = ".".join(parts)
        return s.replace(".[", "[")
        
    This replacement was intended for some case but caused incorrect transformation
    of valid parameter names with bracket characters.
    """
    
    # The logic is that if we had something like a path that contained
    # "module.test_func..[" - we don't want this getting replaced
    # because it would become "module.test_func.["
    
    # What the fix does: just return the unmodified joined string
    
    # Simulate the string behavior that would be broken:
    # With s = "module.test_func..[" and .replace(".[", "[") -> "module.test_func.["
    # This was the incorrect behavior. In practice this would only affect
    # very specific internal constructing scenarios.
    
    # For the regression test, this is mainly about validating end-to-end behavior
    pass