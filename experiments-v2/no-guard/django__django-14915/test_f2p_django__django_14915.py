from django.test import TestCase
from django.forms.models import ModelChoiceIteratorValue


class ModelChoiceIteratorValueHashTest(TestCase):
    def test_model_choice_iterator_value_is_hashable(self):
        """Test that ModelChoiceIteratorValue objects can be used in hash contexts."""
        # Create a ModelChoiceIteratorValue instance
        value = ModelChoiceIteratorValue(value=42, instance="test_instance")
        
        # Before the fix, this would raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        # After the fix, this should work without error
        try:
            # Test that it can be used as a dict key
            test_dict = {value: "test_value"}
            self.assertEqual(test_dict[value], "test_value")
            
            # Test that it can be used in a set
            test_set = {value}
            self.assertIn(value, test_set)
            
            # Test that hash() works
            hash_value = hash(value)
            self.assertIsInstance(hash_value, int)
            
        except TypeError as e:
            if "unhashable type" in str(e):
                self.fail(f"ModelChoiceIteratorValue is not hashable: {e}")
            raise