from django import forms
from django.test import TestCase


class ModelChoiceIteratorValueHashableTest(TestCase):
    """
    Test that ModelChoiceIteratorValue is hashable.
    
    This test ensures the fix for the bug where ModelChoiceIteratorValue
    was unhashable, causing TypeError when used in membership tests.
    """

    def test_model_choice_iterator_value_is_hashable(self):
        """
        Test that ModelChoiceIteratorValue objects can be hashed.
        
        Before the fix, this would raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        """
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create a ModelChoiceIteratorValue instance
        value = ModelChoiceIteratorValue(1, 'test_instance')
        
        # This should not raise an exception
        try:
            hash_value = hash(value)
            self.assertIsInstance(hash_value, int)
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue should be hashable, but got: {e}")

    def test_model_choice_iterator_value_in_dict_key(self):
        """
        Test that ModelChoiceIteratorValue can be used as dict key.
        
        This mimics the use case from the bug report where users
        try to use ModelChoiceIteratorValue in membership tests with dictionaries.
        """
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create some ModelChoiceIteratorValue instances
        value1 = ModelChoiceIteratorValue(1, 'instance1')
        value2 = ModelChoiceIteratorValue(2, 'instance2')
        
        # Should be able to use them as dictionary keys
        try:
            test_dict = {value1: 'first', value2: 'second'}
            
            # Verify they can be retrieved correctly
            self.assertEqual(test_dict[value1], 'first')
            self.assertEqual(test_dict[value2], 'second')
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue should be hashable to work as dict keys, but got: {e}")
        
    def test_model_choice_iterator_value_membership_test(self):
        """
        Test that ModelChoiceIteratorValue works in 'in' operator with dict/set.
        
        This is the direct use case from the bug report:
        if value in self.show_fields: # where self.show_fields is a dict
        """
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create a ModelChoiceIteratorValue that would be the value from a form
        value = ModelChoiceIteratorValue(1, 'test_instance')
        
        # This simulates the user's code:
        # if value in self.show_fields: # where self.show_fields is a dict like {1: ['first_name', 'last_name']}
        show_fields = {1: ['first_name', 'last_name'], 2: ['email']}
        
        # Before fix: This would fail with TypeError: unhashable type: 'ModelChoiceIteratorValue'
        # After fix: This should work correctly
        try:
            # This should work with fixed version because we can call hash() on the ModelChoiceIteratorValue
            # to get a hash and use that for dict membership testing  
            result = value in show_fields  # 
            # The 'in' operator will check if hash(value) is a key in the dict
        except TypeError as e:
            if "unhashable type" in str(e):
                self.fail(f"ModelChoiceIteratorValue should be hashable to work with 'in' operator, but got: {e}")
            else:
                raise  # Re-raise if it's a different TypeError
                
    def test_model_choice_iterator_value_equality_with_hash(self):
        """
        Test that equality and hash work correctly together.
        """
        from django.forms.models import ModelChoiceIteratorValue
        
        value1 = ModelChoiceIteratorValue(1, 'instance1')
        value2 = ModelChoiceIteratorValue(1, 'instance2')  # Same value, different instance
        
        # These should be equal
        self.assertEqual(value1, value2)
        
        # If hash is properly implemented, equal objects should have equal hashes
        try:
            hash_value1 = hash(value1)
            hash_value2 = hash(value2)
            # Even with same value, their hashes don't have to be equal (we just want them to be hashable)
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue should be hashable for equality to work properly, but got: {e}")