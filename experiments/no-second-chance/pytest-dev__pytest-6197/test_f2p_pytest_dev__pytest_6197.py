import pytest


def test_init_py_module_import_should_be_skipped(testdir):
    """
    Test that __init__.py files with import errors don't break test collection.
    
    The regression was that in pytest 5.2.3, __init__.py files under the current 
    directory were being attempted to be imported during collection, even if they 
    contained code that would cause import to fail.
    
    The fix was to ensure that __init__.py files are properly handled and not
    imported during collection process.
    """
    
    # Create a simple working test file
    testdir.makepyfile(
        test_simple="""
        def test_simple():
            assert True
        """
    )
    
    # Create a package directory with an __init__.py that has import issues
    testdir.mkpydir("problematic_package")
    
    # This __init__.py should not be imported during normal test collection
    # but in buggy versions it would attempt to be imported, failing with AssertionError
    testdir.makepyfile(
        problematic_package__init__="""
        # This should cause import to fail when accessed during collection
        assert False, "This __init__.py file should not be imported during collection"
        """
    )
    
    # Run pytest - should not fail on collection due to problematic __init__.py
    result = testdir.runpytest()
    
    # This test must pass (indicating the bug is fixed)
    # Before the fix, this would result in:
    # ERROR collecting problematic_package/__init__.py
    # problematic_package/__init__.py:2: in <module> 
    #     assert False, "This __init__.py file should not be imported during collection"
    # E   AssertionError
    assert result.ret == 0


def test_multiple_problematic_init_files(testdir):
    """
    Test that multiple packages with problematic __init__.py files are handled properly.
    """
    
    # Create working test files
    testdir.makepyfile(
        test_a="""
        def test_a():
            assert True
        """
    )
    
    testdir.makepyfile(
        test_b="""
        def test_b():
            assert True
        """
    )
    
    # Create multiple packages with problematic __init__.py files
    testdir.mkpydir("package1")
    testdir.mkpydir("package2") 
    
    testdir.makepyfile(
        package1__init__="""
        assert False, "package1 should not be imported"
        """
    )
    
    testdir.makepyfile(
        package2__init__="""
        assert False, "package2 should not be imported"  
        """
    )
    
    # Collecting tests should work even if there are import-blocking __init__.py files
    result = testdir.runpytest()
    
    # Should pass (tests collected successfully)
    assert result.ret == 0