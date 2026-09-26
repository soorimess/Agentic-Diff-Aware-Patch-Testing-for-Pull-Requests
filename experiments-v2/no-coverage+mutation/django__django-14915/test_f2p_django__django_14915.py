import unittest

from django import forms


class ModelChoiceIteratorValueHashTest(unittest.TestCase):
    def test_model_choice_iterator_value_is_hashable(self):
        """
        Regression test for Django #14915.
        ModelChoiceIteratorValue should be hashable to allow use in 'in' operations.
        """
        # Import the class directly from the module where it's defined
        from django.forms.models import ModelChoiceIteratorValue
        
        # Test 1: Basic hashability
        value = "test_value"
        instance = "test_instance"
        
        # Create ModelChoiceIteratorValue instance
        iterator_value = ModelChoiceIteratorValue(value, instance)
        
        # Before the fix, this would raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        # After the fix, this should work fine
        try:
            hash_value = hash(iterator_value)
            # If we get here without exception, the object is hashable
            self.assertIsNotNone(hash_value)
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue is not hashable: {e}")
        
        # Test 2: The main use case from the bug report - 'in' operator
        # This is what fails when the object is not hashable
        test_dict = {value: ['first_name', 'last_name']}
        
        # This should work without raising TypeError
        self.assertIn(iterator_value, test_dict)  # This would fail before the fix
        
        # Test 3: Equality behavior
        other_iterator_value = ModelChoiceIteratorValue(value, instance)
        self.assertEqual(iterator_value, other_iterator_value)
        
        # Test 4: Hash consistency
        self.assertEqual(hash(iterator_value), hash(other_iterator_value))
        
        # Test 5: Different values have different behavior
        different_iterator_value = ModelChoiceIteratorValue("different_value", instance)
        self.assertNotEqual(iterator_value, different_iterator_value)
        
        # Test 6: Ensure it works in a more realistic scenario
        # This simulates what happens in create_option method mentioned in bug report
        show_fields = {value: ['first_name', 'last_name']}
        self.assertIn(iterator_value, show_fields)