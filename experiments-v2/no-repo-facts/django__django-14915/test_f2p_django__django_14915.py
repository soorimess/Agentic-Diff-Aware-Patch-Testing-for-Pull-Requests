"""
Regression test for Django issue where ModelChoiceIteratorValue is not hashable.
This test ensures that ModelChoiceIteratorValue can be used in hash-based operations
like being a dictionary key or in a set.
"""
from django.forms.models import ModelChoiceIteratorValue
from django.test import TestCase


class ModelChoiceIteratorValueHashTest(TestCase):
    def test_model_choice_iterator_value_is_hashable(self):
        """
        Test that ModelChoiceIteratorValue instances can be hashed.
        This is needed for operations like 'value in dict' or 'value in set'.
        """
        # Create a simple ModelChoiceIteratorValue instance
        value = ModelChoiceIteratorValue("test_value", "test_instance")
        
        # This should not raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        # before the fix, but should work after the fix
        try:
            hash_value = hash(value)
            self.assertIsNotNone(hash_value)
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue is not hashable: {e}")
    
    def test_model_choice_iterator_value_in_dict_key(self):
        """
        Test that ModelChoiceIteratorValue can be used as a dictionary key.
        This is the specific case mentioned in the bug report.
        """
        # Create a ModelChoiceIteratorValue instance
        value = ModelChoiceIteratorValue(1, "test_instance")
        
        # This should work without raising TypeError
        test_dict = {value: "some_value"}
        self.assertEqual(test_dict[value], "some_value")
    
    def test_model_choice_iterator_value_in_set(self):
        """
        Test that ModelChoiceIteratorValue can be used in a set.
        """
        # Create ModelChoiceIteratorValue instances
        value1 = ModelChoiceIteratorValue(1, "test_instance_1")
        value2 = ModelChoiceIteratorValue(1, "test_instance_2")  # Same value, different instance
        
        # This should work without raising TypeError
        test_set = {value1, value2}
        self.assertEqual(len(test_set), 1)  # Should be deduplicated due to equality
        
        # Test with different values
        value3 = ModelChoiceIteratorValue(2, "test_instance_3")
        test_set2 = {value1, value3}
        self.assertEqual(len(test_set2), 2)
    
    def test_model_choice_iterator_value_hash_correctness(self):
        """
        Test that hash values are computed correctly based on the value attribute.
        """
        # Test with string values
        value1 = ModelChoiceIteratorValue("test", "instance1")
        value2 = ModelChoiceIteratorValue("test", "instance2")
        
        # They should be equal
        self.assertEqual(value1, value2)
        
        # They should have the same hash (this is required for hash consistency)
        self.assertEqual(hash(value1), hash(value2))
        
        # Test with integer values
        int_value1 = ModelChoiceIteratorValue(42, "instance")
        int_value2 = ModelChoiceIteratorValue(42, "another_instance")
        self.assertEqual(hash(int_value1), hash(int_value2))
        
        # Test with None values
        none_value1 = ModelChoiceIteratorValue(None, "instance")
        none_value2 = ModelChoiceIteratorValue(None, "another_instance")
        self.assertEqual(hash(none_value1), hash(none_value2))
        
        # Test that different values produce different hashes (not guaranteed but likely)
        str_value = ModelChoiceIteratorValue("string", "instance")
        int_value = ModelChoiceIteratorValue(123, "instance")
        # Different values should generally have different hashes (though collisions are possible)
        # We're mainly checking that they don't raise exceptions
        hash(str_value)
        hash(int_value)