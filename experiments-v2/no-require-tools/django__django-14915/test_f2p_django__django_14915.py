from django.test import TestCase
from django import forms


class ModelChoiceIteratorValueHashTest(TestCase):
    """Test that ModelChoiceIteratorValue is hashable."""
    
    def test_model_choice_iterator_value_is_hashable(self):
        """Test that ModelChoiceIteratorValue can be used as dict key."""
        # Create a simple object to use as instance
        class DummyInstance:
            def __init__(self, value):
                self.value = value
                
            def __str__(self):
                return f"DummyInstance({self.value})"
        
        # Create a ModelChoiceIteratorValue instance
        instance = DummyInstance("test_instance")
        value = "test_value"
        iterator_value = forms.models.ModelChoiceIteratorValue(value, instance)
        
        # This should not raise TypeError: unhashable type
        # The bug was that this would fail with "TypeError: unhashable type: 'ModelChoiceIteratorValue'"
        # This simulates the use case from the bug report: value in self.show_fields
        test_dict = {iterator_value: "some_value"}
        
        # Verify we can access it
        self.assertEqual(test_dict[iterator_value], "some_value")
        
        # Also test that it works in 'in' operations with dicts (as described in bug report)
        show_fields = {iterator_value: ['first_name', 'last_name']}
        self.assertIn(iterator_value, show_fields)
        
    def test_model_choice_iterator_value_equality_and_hash_consistency(self):
        """Test that equality and hash are consistent."""
        class DummyInstance:
            def __init__(self, value):
                self.value = value
                
            def __str__(self):
                return f"DummyInstance({self.value})"
        
        instance1 = DummyInstance("test1")
        instance2 = DummyInstance("test2")
        value = "test_value"
        
        iterator_value1 = forms.models.ModelChoiceIteratorValue(value, instance1)
        iterator_value2 = forms.models.ModelChoiceIteratorValue(value, instance2)
        
        # These should be equal (same value)
        self.assertEqual(iterator_value1, iterator_value2)
        
        # And they should have the same hash (since they have the same value)
        # This should not raise TypeError: unhashable type
        self.assertEqual(hash(iterator_value1), hash(iterator_value2))