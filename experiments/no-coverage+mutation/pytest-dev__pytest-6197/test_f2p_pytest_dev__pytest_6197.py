"""
Regression test for pytest issue: 
Regression in 5.2.3: pytest tries to collect random __init__.py files

This is a simple test to demonstrate:
1. In the buggy code (before change): __init__.py files get processed normally
2. In the fixed code (after change): __init__.py files have special handling to prevent importing

The test focuses on the core change: 
- Module.__init__ used to set _ALLOW_MARKERS = False for __init__.py files
- This prevented importing during collection
"""
import pytest


def test_init_py_files_that_cannot_be_imported_do_not_break_collection(testdir):
    """
    The root issue from the bug report: when pytest 5.2.3 encounters a __init__.py 
    that fails during import, it attempts to import it, causing collection to fail.
    
    This test ensures that such __init__.py files are processed in a way that 
    doesn't attempt to import them (when they're not directly part of the test path).
    """
        
    # Create a structure exactly as described in bug report:
    # mkdir foobar
    # echo 'assert False' >! foobar/__init__.py  
    foobar_dir = testdir.mkdir("foobar")
    bad_init = foobar_dir.join("__init__.py") 
    bad_init.write("assert False")
    
    # Create a test file that should run  
    test_file = testdir.makepyfile("""
def test_something():
    assert True
""")
    
    # Run pytest - in buggy version, we see error about collecting foobar/__init__.py
    # in fixed version, this should complete without error about that file
    
    # The test works by relying on the fact that these types of tests will fail
    # in both cases EXCEPT when they current behavior is properly adhere to in one case
    
    # Actually, since we know the codebase currently has the fix in place,
    # any usage that tries to import __init__.py files (expecting problems) would be wrong
    # But we'll implement a minimal assertion to make it meaningful
    
    result = testdir.runpytest("-v", "--collect-only")
    
    # Whatever any specific error in the scenario is, if the code has the fix it shouldn't
    # show an ERROR collecting __init__.py for the foobar directory
    # (this would indicate the old buggy behavior in the actual test scenario)
    if "ERROR collecting foobar/__init__.py" in result.stderr:
        # This means the old buggy behavior is present - the test will fail
        # to properly detect what would have been the main passing scenario
        pytest.fail("Bug still present: foobar/__init__.py was collected and tried to import")
    
    # If we get here, that means __init__.py was not collected as a test module
    # which is the expected, fixed behavior
    result.assert_outcomes(passed=1)  # Only our test should pass