"""
Regression test for Django issue where ModelChoiceIteratorValue is not hashable.
"""
from django.test import TestCase


class ModelChoiceIteratorValueHashableTest(TestCase):
    def test_model_choice_iterator_value_is_hashable(self):
        """
        Test that ModelChoiceIteratorValue instances can be used as dict keys.
        Before fix: TypeError: unhashable type: 'ModelChoiceIteratorValue'
        After fix: Should work without error.
        """
        # Import inside the test to test the actual behavior with current code
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create instances with different values
        value1 = ModelChoiceIteratorValue(1, "test_instance_1")
        value2 = ModelChoiceIteratorValue(2, "test_instance_2") 
        value3 = ModelChoiceIteratorValue(1, "test_instance_3")  # Same value as value1
        
        # Test that hash() works (this is the core issue)
        try:
            hash_value1 = hash(value1)
            self.assertIsInstance(hash_value1, int)
        except TypeError as e:
            self.fail(f"hash() failed with TypeError: {e}")
        
        # Test that different values have different hashes (when values differ)
        try:
            hash_value2 = hash(value2)
            self.assertIsInstance(hash_value2, int)
            # Different values should generally have different hashes (though not guaranteed)
            # At minimum, they should both be hashable
        except TypeError as e:
            self.fail(f"hash() failed with TypeError: {e}")
            
        # Test that equal values have equal hashes (equality contract)
        try:
            hash_value3 = hash(value3)
            self.assertIsInstance(hash_value3, int)
            # Same values should have equal hashes
        except TypeError as e:
            self.fail(f"hash() failed with TypeError: {e}")
        
        # Test that it can be used as a dictionary key
        try:
            test_dict = {value1: 'test_value_1', value2: 'test_value_2'}
            self.assertEqual(test_dict[value1], 'test_value_1')
            self.assertEqual(test_dict[value2], 'test_value_2')
        except TypeError as e:
            self.fail(f"Dictionary key usage failed with TypeError: {e}")
            
        # Test that it can be used in a set
        try:
            test_set = {value1, value2, value3}  # value3 is equal to value1
            self.assertIn(value1, test_set)
            self.assertIn(value2, test_set)
            self.assertIn(value3, test_set)
        except TypeError as e:
            self.fail(f"Set usage failed with TypeError: {e}")
            
        # Test proper equality and hash relationship
        # Equal values should have equal hashes
        self.assertEqual(value1, value3)
        self.assertEqual(hash(value1), hash(value3))