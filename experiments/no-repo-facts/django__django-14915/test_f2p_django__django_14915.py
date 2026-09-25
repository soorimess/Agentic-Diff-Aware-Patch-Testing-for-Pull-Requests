"""
Regression test for Django issue #14915: ModelChoiceIteratorValue should be hashable.
"""
from django.test import TestCase
from django.forms.models import ModelChoiceIteratorValue

class ModelChoiceIteratorValueHashableTest(TestCase):
    
    def test_model_choice_iterator_value_is_hashable(self):
        """Test that ModelChoiceIteratorValue instances are hashable."""
        # Create a ModelChoiceIteratorValue as it would be used in real code
        value = ModelChoiceIteratorValue('test_value', 'test_instance')
        
        # This should not raise TypeError: unhashable type
        hash_value = hash(value)
        self.assertIsInstance(hash_value, int)
    
    def test_model_choice_iterator_value_hash_consistency(self):
        """Test that hash values are consistent for equal objects."""
        value1 = ModelChoiceIteratorValue('test_value', 'test_instance1')
        value2 = ModelChoiceIteratorValue('test_value', 'test_instance2')
        
        # Equal values should have equal hash values
        self.assertEqual(hash(value1), hash(value2))
        
    def test_model_choice_iterator_value_in_dict_keys(self):
        """Test that ModelChoiceIteratorValue can be used as dict keys."""
        value = ModelChoiceIteratorValue('test_value', 'test_instance')
        
        # This should work without TypeError
        test_dict = {value: 'some_value'}
        self.assertEqual(test_dict[value], 'some_value')
        
    def test_model_choice_iterator_value_in_sets(self):
        """Test that ModelChoiceIteratorValue can be used in sets."""
        value1 = ModelChoiceIteratorValue('test_value', 'test_instance1')
        value2 = ModelChoiceIteratorValue('test_value', 'test_instance2')
        
        # Should be able to put in set and test membership
        test_set = {value1, value2}
        self.assertIn(value1, test_set)
        self.assertIn(value2, test_set)