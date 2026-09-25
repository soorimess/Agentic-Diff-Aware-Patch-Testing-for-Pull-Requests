"""
Regression test for Django issue where ModelChoiceIteratorValue is not hashable.
This test verifies that ModelChoiceIteratorValue can be used in hash contexts.
"""
from django.test import TestCase


class ModelChoiceIteratorValueHashTest(TestCase):
    def test_model_choice_iterator_value_is_hashable(self):
        """
        Test that ModelChoiceIteratorValue instances are hashable.
        Before the fix, this would raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        """
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create a ModelChoiceIteratorValue instance (similar to how it's created in forms)
        value_instance = ModelChoiceIteratorValue("test_value", "test_instance")
        
        # This should not raise TypeError - it should work after fix
        try:
            hash_value = hash(value_instance)
            self.assertIsNotNone(hash_value)
        except TypeError as e:
            self.fail(f"hash() raised TypeError unexpectedly: {e}")

    def test_model_choice_iterator_value_hash_returns_correct_value(self):
        """
        Test that hash of ModelChoiceIteratorValue returns hash of the underlying value.
        This ensures the implementation is correct, not just that it doesn't crash.
        """
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create instances with different values
        value1 = ModelChoiceIteratorValue(123, "instance1")
        value2 = ModelChoiceIteratorValue(123, "instance2")  # Same value, different instance
        value3 = ModelChoiceIteratorValue(456, "instance3")
        
        # They should have the same hash since they have the same value
        hash1 = hash(value1)
        hash2 = hash(value2) 
        self.assertEqual(hash1, hash2)
        
        # Different values should have different hashes
        hash3 = hash(value3)
        self.assertNotEqual(hash1, hash3)

    def test_model_choice_iterator_value_in_dict_membership(self):
        """
        Test that ModelChoiceIteratorValue instances can be used for membership checking.
        This reproduces the specific issue from the bug report where 'value in dict' fails.
        """
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create a ModelChoiceIteratorValue instance 
        value_instance = ModelChoiceIteratorValue(123, "test_instance")
        
        # Test using the pattern from bug report: 'value in dict'  
        test_dict = {123: ['first_name', 'last_name']}
        
        # This should not raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        try:
            in_dict = value_instance in test_dict
            # We don't expect it to be found since the key is 123, not a ModelChoiceIteratorValue
            # But it should not crash with TypeError
        except TypeError as e:
            self.fail(f"'in' operator raised TypeError unexpectedly: {e}")

    def test_model_choice_iterator_value_equality_and_hash_consistency(self):
        """
        Test that equality and hash behavior is consistent for ModelChoiceIteratorValue.
        """
        from django.forms.models import ModelChoiceIteratorValue
        
        value1 = ModelChoiceIteratorValue("test_value", "instance1")
        value2 = ModelChoiceIteratorValue("test_value", "instance2")
        
        # They should be equal because they have same value 
        self.assertEqual(value1, value2)
        
        # If they are equal, they should have the same hash (if hashable)
        try:
            hash1 = hash(value1)
            hash2 = hash(value2)
            self.assertEqual(hash1, hash2)
        except TypeError as e:
            self.fail(f"Hash consistency test failed: {e}")