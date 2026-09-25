"""
Regression test for Django issue: ModelChoiceIteratorValue is not hashable.

This test ensures that ModelChoiceIteratorValue objects can be used as
dictionary keys or in sets, which requires them to be hashable.
"""
from django.test import TestCase


class ModelChoiceIteratorValueHashTest(TestCase):
    def test_model_choice_iterator_value_is_hashable(self):
        """
        Test that ModelChoiceIteratorValue objects can be hashed.
        
        Before the fix, this would raise a TypeError: unhashable type: 'ModelChoiceIteratorValue'
        """
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create a simple ModelChoiceIteratorValue instance
        value = ModelChoiceIteratorValue("test_value", "test_instance")
        
        # This should not raise an exception
        hash_value = hash(value)
        
        # Verify that hashing works correctly (values should be consistent)
        self.assertEqual(hash_value, hash(value))
        
        # Test that instances with same values are equal and have same hash
        value2 = ModelChoiceIteratorValue("test_value", "test_instance")
        self.assertEqual(value, value2)
        self.assertEqual(hash(value), hash(value2))
        
        # Test that instances with different values have different hashes
        value3 = ModelChoiceIteratorValue("different_value", "test_instance")
        self.assertNotEqual(value, value3)
        
    def test_model_choice_iterator_value_hash_derived_from_value(self):
        """
        Test that ModelChoiceIteratorValue hash is derived from its value field,
        not from some other arbitrary source.
        """
        from django.forms.models import ModelChoiceIteratorValue
        
        # Ensure that hash() result is consistent with the underlying value
        value1 = ModelChoiceIteratorValue("same_value", "different_instance1")
        value2 = ModelChoiceIteratorValue("same_value", "different_instance2") 
        
        # Both should have same hash since they have same value
        self.assertEqual(hash(value1), hash(value2))
        
        # But different values should have different hashes
        value3 = ModelChoiceIteratorValue("different_value", "some_instance")
        self.assertNotEqual(hash(value1), hash(value3))
        
    def test_model_choice_iterator_value_in_set(self):
        """Test that ModelChoiceIteratorValue objects can be used in sets."""
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create a few ModelChoiceIteratorValue instances
        value1 = ModelChoiceIteratorValue("val1", "obj1")
        value2 = ModelChoiceIteratorValue("val2", "obj2")
        value3 = ModelChoiceIteratorValue("val1", "obj1")  # Same as value1
        
        # This should work without raising an exception
        my_set = {value1, value2, value3}
        
        # Should contain 2 unique items (value3 equals value1)
        self.assertEqual(len(my_set), 2)
        
    def test_model_choice_iterator_value_in_dict(self):
        """Test that ModelChoiceIteratorValue objects can be used as dict keys."""
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create a few ModelChoiceIteratorValue instances
        value1 = ModelChoiceIteratorValue("val1", "obj1")
        value2 = ModelChoiceIteratorValue("val2", "obj2")
        
        # This should work without raising an exception
        my_dict = {value1: "first", value2: "second"}
        
        # Verify we can retrieve values correctly
        self.assertEqual(my_dict[value1], "first")
        self.assertEqual(my_dict[value2], "second")