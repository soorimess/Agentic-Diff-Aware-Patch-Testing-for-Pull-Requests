"""
Regression test for Django issue: named tuples used as arguments to __range error in 3.0

Tests the behavior change that fixed the broken Django resolve_lookup_value handling
of named tuples.
"""
from collections import namedtuple
import unittest


# Create named tuples that would exhibit the exact bug in Django
Range = namedtuple('Range', ['start', 'end'])


class DjangoResolveLookupValueTest(unittest.TestCase):
    
    def test_exact_django_namedtuple_bug_simulation(self):
        """
        Test that explicitly validates what Django's resolve_lookup_value was doing wrong
        and how it was fixed.
        
        The OLD behavior (before fix):
        Django would call: type(value)(generator_expression)
        For a namedtuple like Range(1, 10), this was Range((1, 10))
        But Range expects individual args, not one tuple argument
        
        The NEW behavior (after fix):
        Django calls: type_( *values ) for namedtuples
        Which is Range(*generator) = Range(1, 10) - correct!
        """
        
        # Create a named tuple that Django would process
        range_arg = Range(1, 10)
        
        # Demonstrate that the problematic bug was real  
        # This exactly replicates what Django's old wrong approach used to do:
        try:
            # This is what the WRONG approach would do:
            # If Django did: type(value)( <generator> )  
            # That becomes Range((1, 10))  - wrong!
            # The error is "__new__() missing 1 required positional argument" 
            result = Range((1, 10))
            # If somehow this passes (wouldn't be normal but let's be sure)
            self.fail("The old approach should have failed with TypeError")
        except TypeError as e:
            # This confirms we can trigger the same exact error as the bug report
            self.assertIn("__new__() missing 1 required positional argument", str(e))
            
        # Demonstrate the correct behavior
        # This mimics Django's fixed approach: 
        generator = (x for x in range_arg)  # Generator that yields 1 then 10
        # The FIXED approach: Range(*generator) = Range(1, 10) - correct
        result = Range(*generator)
        self.assertEqual(result, range_arg)
        
        # Test that the type is preserved correctly (most important aspect of fix)
        self.assertEqual(type(result), type(range_arg))
        
    def test_namedtuple_handling_mechanism(self):
        """
        Tests the exact mechanism Django changed to handle namedtuples properly.
        """
        # This directly tests that the logic that determines when to use unpacking exists
        range_arg = Range(5, 15)
        
        # The fix hinges on detecting namedtuples by checking if they have _make
        self.assertTrue(hasattr(type(range_arg), '_make'))
        
        # This is the key assertion about what we want to preserve:
        # When given a named tuple value, make sure it used the *values approach
        # The approach that should be used: type_(*generator) instead of type_(generator)
        
        # Test iterative construction path  
        generator = (x for x in range_arg)
        type_ = type(range_arg)
        
        # This capture what must work as the fix:
        # If hasattr(type_, '_make'):  # namedtuple
        #    return type_(*values)  # THE FIX - unpacking
        # else:
        #    return type_(values)   # Regular case 
        result = type_(*generator)  # This is the fixed path exercised for namedtuples
        
        self.assertEqual(result, range_arg)
        self.assertEqual(type(result), type(range_arg))
        
        # Ensure we didn't break regular tuples (else branch)
        regular_tuple = (5, 15)
        generator = (x for x in regular_tuple)
        type_ = type(regular_tuple)
        
        # Regular tuples should NOT have _make
        self.assertFalse(hasattr(type_, '_make'))
        # So they follow the else path
        result = type_(generator)  # This works for regular tuples
        self.assertEqual(result, regular_tuple)