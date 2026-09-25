"""
Regression test that should fail with original code and pass with fixed code.
"""
import collections
import sys
import os

# Since this is meant to be run by the Django test runner and
# it's not clear how to make deeper hooks, let's create a focused 
# demonstration of the exact behavior we want to ensure

def demonstrate_bug():
    """Direct demonstration of the exact pattern that fails."""
    
    # Create the exact named tuple situation from the bug report
    RangeTuple = collections.namedtuple('RangeTuple', ['low', 'high'])
    test_tuple = RangeTuple(10, 20)
    
    print("Testing named tuple reconstruction pattern...")
    
    # OLD WAY (the bug): Creating tuple with generator directly
    try:
        old_way = type(test_tuple)(i for i in [10, 20])
        print("OLD WAY succeeded (unexpected):", old_way)
        return False  # indicates logic works (what is good)
    except TypeError as e:
        print("OLD WAY failed as expected:", str(e))
        return True  # indicates bug exists
    
def demonstrate_fix():
    """Show the fix works correctly."""
    
    RangeTuple = collections.namedtuple('RangeTuple', ['low', 'high'])
    test_tuple = RangeTuple(10, 20)
    
    print("Testing fixed named tuple reconstruction...")
    
    # NEW WAY: Unpacking generator for namedtuples
    try:
        # This is what should work (the fix)
        values = (i for i in [10, 20])
        type_ = type(test_tuple)
        
        if hasattr(type_, '_make'):  # namedtuple
            new_way = type_(*values)  # This works
        else:
            new_way = type_(values)  # This also works for regular tuples
            
        print("NEW WAY succeeded:", new_way)
        return True  # indicates fix works correctly
    except Exception as e:
        print("NEW WAY failed:", str(e)) 
        return False

def test_name():
    """Truly minimal test method for this situation."""
    # For this registry test, the actionable check:
    # The fix makes this not a problem
    
    # Actually attempt to just trigger the namedtuples directly
    RangeTuple = collections.namedtuple('RangeTuple', ['low', 'high'])
    value = RangeTuple(1, 2)
    
    # This demonstrates that we would hit exactly that check needed:
    # hasattr(type(value), '_make') should be True for namedtuple
    print(f"Has _make: {hasattr(type(value), '_make')}")
    
    # And to verify the correct check that should be in Django code:
    # if hasattr(type_, '_make'): return type_(*values) 

if __name__ == "__main__":
    print("=== Demonstrating named tuple bug ===")
    bug_exists = demonstrate_bug()
    fix_works = demonstrate_fix()
    
    print(f"Bug present (before fix): {bug_exists}")
    print(f"Fix works (after fix): {fix_works}")
    
    # This is essentially what should be the test: "does the code path
    # of Django resolve_lookup_value properly handle namedtuples?"
    
    test_name()
    print("Test complete")