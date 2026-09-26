import unittest

from django.forms.models import ModelChoiceIteratorValue


class ModelChoiceIteratorValueHashTest(unittest.TestCase):
    """Test that ModelChoiceIteratorValue is hashable."""
    
    def test_model_choice_iterator_value_is_hashable(self):
        """Test that ModelChoiceIteratorValue instances can be hashed."""
        # Create a simple value and instance to test with
        value = 42
        instance = "test_instance"
        
        # Create a ModelChoiceIteratorValue instance
        mci_value = ModelChoiceIteratorValue(value, instance)
        
        # This should not raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        try:
            hash_value = hash(mci_value)
            # If we get here without exception, it's hashable
            self.assertIsInstance(hash_value, int)
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue is not hashable: {e}")
    
    def test_model_choice_iterator_value_in_set(self):
        """Test that ModelChoiceIteratorValue can be used in sets."""
        # Create simple values to test with
        value1 = 42
        value2 = 43
        instance1 = "test_instance_1"
        instance2 = "test_instance_2"
        
        # Create ModelChoiceIteratorValue instances
        mci_value1 = ModelChoiceIteratorValue(value1, instance1)
        mci_value2 = ModelChoiceIteratorValue(value2, instance2)
        
        # This should work without TypeError
        my_set = {mci_value1, mci_value2}
        self.assertEqual(len(my_set), 2)
        
        # Test with duplicate values (should be treated as same due to __eq__ implementation)
        mci_value1_duplicate = ModelChoiceIteratorValue(value1, instance1)
        my_set_with_duplicate = {mci_value1, mci_value1_duplicate}
        self.assertEqual(len(my_set_with_duplicate), 1)
    
    def test_model_choice_iterator_value_in_dict(self):
        """Test that ModelChoiceIteratorValue can be used as dict keys."""
        # Create simple values to test with
        value1 = 42
        value2 = 43
        instance1 = "test_instance_1"
        instance2 = "test_instance_2"
        
        # Create ModelChoiceIteratorValue instances
        mci_value1 = ModelChoiceIteratorValue(value1, instance1)
        mci_value2 = ModelChoiceIteratorValue(value2, instance2)
        
        # This should work without TypeError
        my_dict = {mci_value1: 'first', mci_value2: 'second'}
        self.assertEqual(len(my_dict), 2)
        self.assertEqual(my_dict[mci_value1], 'first')
        self.assertEqual(my_dict[mci_value2], 'second')
        
        # Test with duplicate keys
        mci_value1_duplicate = ModelChoiceIteratorValue(value1, instance1)
        my_dict_with_duplicate = {mci_value1: 'first', mci_value1_duplicate: 'duplicate'}
        self.assertEqual(len(my_dict_with_duplicate), 1)
        self.assertEqual(my_dict_with_duplicate[mci_value1], 'duplicate')