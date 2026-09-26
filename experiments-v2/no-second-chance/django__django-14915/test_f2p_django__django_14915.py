import unittest

from django.forms.models import ModelChoiceIteratorValue


class ModelChoiceIteratorValueHashTest(unittest.TestCase):
    def test_model_choice_iterator_value_is_hashable(self):
        """Test that ModelChoiceIteratorValue instances are hashable."""
        # Create a ModelChoiceIteratorValue instance
        value = ModelChoiceIteratorValue(42, "test_instance")
        
        # This should not raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        # before the fix, it would raise this error
        try:
            hash_value = hash(value)
            # If we get here without exception, the object is hashable
            self.assertIsNotNone(hash_value)
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue is not hashable: {e}")
    
    def test_model_choice_iterator_value_hash_consistency(self):
        """Test that ModelChoiceIteratorValue hash is consistent with its value."""
        # Create two instances with the same value
        value1 = ModelChoiceIteratorValue(42, "test_instance1")
        value2 = ModelChoiceIteratorValue(42, "test_instance2")
        
        # They should have the same hash since they have the same value
        self.assertEqual(hash(value1), hash(value2))
        
        # Create an instance with a different value
        value3 = ModelChoiceIteratorValue(43, "test_instance3")
        # Should have a different hash
        self.assertNotEqual(hash(value1), hash(value3))
    
    def test_model_choice_iterator_value_in_dict_key(self):
        """Test that ModelChoiceIteratorValue can be used as a dict key."""
        # Create ModelChoiceIteratorValue instances
        value1 = ModelChoiceIteratorValue(1, "instance1")
        value2 = ModelChoiceIteratorValue(2, "instance2")
        
        # This should work without raising TypeError
        test_dict = {value1: "first", value2: "second"}
        
        # Verify the dict works correctly
        self.assertEqual(test_dict[value1], "first")
        self.assertEqual(test_dict[value2], "second")
    
    def test_model_choice_iterator_value_in_set(self):
        """Test that ModelChoiceIteratorValue can be used in a set."""
        # Create ModelChoiceIteratorValue instances
        value1 = ModelChoiceIteratorValue(1, "instance1")
        value2 = ModelChoiceIteratorValue(2, "instance2")
        value3 = ModelChoiceIteratorValue(1, "instance3")  # Same value as value1
        
        # This should work without raising TypeError
        test_set = {value1, value2, value3}
        
        # Sets should deduplicate based on equality, not identity
        # value1 and value3 should be considered equal since they have the same value
        self.assertEqual(len(test_set), 2)  # Should contain 2 unique items