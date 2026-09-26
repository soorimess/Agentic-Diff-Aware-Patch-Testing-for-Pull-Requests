from django.test import TestCase
from django.forms.models import ModelChoiceIteratorValue


class ModelChoiceIteratorValueHashTest(TestCase):
    def test_model_choice_iterator_value_is_hashable(self):
        """Test that ModelChoiceIteratorValue instances are hashable."""
        # Create a ModelChoiceIteratorValue instance
        value = ModelChoiceIteratorValue(1, "test_instance")
        
        # This should not raise a TypeError: unhashable type
        # It should be possible to use it in sets or as dict keys
        test_set = {value}
        self.assertIn(value, test_set)
        
        # Also test with dict
        test_dict = {value: "test_value"}
        self.assertEqual(test_dict[value], "test_value")
        
        # Test that hash works correctly
        hash_value = hash(value)
        self.assertIsInstance(hash_value, int)
        
        # Test that equal values have equal hashes
        value2 = ModelChoiceIteratorValue(1, "another_instance")
        self.assertEqual(hash(value), hash(value2))