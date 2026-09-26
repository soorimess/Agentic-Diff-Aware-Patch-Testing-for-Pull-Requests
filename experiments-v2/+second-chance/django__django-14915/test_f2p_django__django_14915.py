from django import forms
from django.test import TestCase
from django.forms.models import ModelChoiceIteratorValue


class ModelChoiceIteratorValueHashTest(TestCase):
    def test_model_choice_iterator_value_is_hashable(self):
        """Test that ModelChoiceIteratorValue is hashable after the fix."""
        # Create a ModelChoiceIteratorValue instance
        value = ModelChoiceIteratorValue(value=1, instance="test_instance")
        
        # Before the fix, this would raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        # After the fix, this should work fine
        try:
            hash_value = hash(value)
            self.assertIsNotNone(hash_value)
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue is not hashable: {e}")

    def test_model_choice_iterator_value_in_dict_key(self):
        """Test that ModelChoiceIteratorValue can be used as dict key."""
        # Create ModelChoiceIteratorValue instances
        value1 = ModelChoiceIteratorValue(value=1, instance="test_instance_1")
        value2 = ModelChoiceIteratorValue(value=2, instance="test_instance_2")
        
        # Create a dictionary with ModelChoiceIteratorValue as keys
        test_dict = {value1: "first", value2: "second"}
        
        # This should work after the fix
        self.assertEqual(test_dict[value1], "first")
        self.assertEqual(test_dict[value2], "second")

    def test_model_choice_iterator_value_in_set(self):
        """Test that ModelChoiceIteratorValue can be used in a set."""
        # Create ModelChoiceIteratorValue instances
        value1 = ModelChoiceIteratorValue(value=1, instance="test_instance_1")
        value2 = ModelChoiceIteratorValue(value=2, instance="test_instance_2")
        
        # Create a set with ModelChoiceIteratorValue instances
        test_set = {value1, value2}
        
        # This should work after the fix
        self.assertIn(value1, test_set)
        self.assertIn(value2, test_set)
        
    def test_model_choice_iterator_value_equality_and_hash_consistency(self):
        """Test that equality and hash are consistent."""
        value1 = ModelChoiceIteratorValue(value=1, instance="test_instance_1")
        value2 = ModelChoiceIteratorValue(value=1, instance="test_instance_2")  # Same value, different instance
        
        # These should be equal
        self.assertEqual(value1, value2)
        
        # And they should have the same hash (since they have the same value)
        self.assertEqual(hash(value1), hash(value2))
        
    def test_model_choice_iterator_value_different_values_have_different_hashes(self):
        """Test that different values have different hashes."""
        value1 = ModelChoiceIteratorValue(value=1, instance="test_instance_1")
        value2 = ModelChoiceIteratorValue(value=2, instance="test_instance_2")
        
        # Different values should have different hashes
        self.assertNotEqual(hash(value1), hash(value2))