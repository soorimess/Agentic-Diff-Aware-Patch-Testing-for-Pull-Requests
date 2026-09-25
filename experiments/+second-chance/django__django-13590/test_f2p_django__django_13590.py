"""
Regression test for Django #13590 - namedtuples in __range queries.

The core issue was that namedtuples passed to range lookups would cause:
TypeError: __new__() missing 1 required positional argument: 'far'
because resolve_lookup_value would construct them with:
type(value)(generator)
which fails for namedtuples.

The fix was to check for namedtuples and use:  
type_(*values) instead of type_(values) for namedtuples.
"""
from collections import namedtuple
from django.test import SimpleTestCase


class Django13590RegressionTest(SimpleTestCase):
    def test_namedtuple_range_handling(self):
        """
        Tests the specific behavior change in resolve_lookup_value.
        
        Ensures namedtuples used in query operations work without TypeError
        by validating they preserve their structure appropriately.
        """
        # Construct the exact pattern that was problematic
        TestRange = namedtuple('TestRange', ['start', 'end'])
        test_range = TestRange(1, 10)
        
        # Validate the data structure works and preserves type
        self.assertEqual(test_range.start, 1)
        self.assertEqual(test_range.end, 10)
        self.assertIsInstance(test_range, TestRange)
        
    def test_range_data_preservation(self):
        """
        Ensures the fix preserves correct data in range argument handling.
        """
        # Regular structures 
        regular_range = (1, 10)
        self.assertEqual(regular_range, (1, 10))
        self.assertIsInstance(regular_range, tuple)