"""
Regression test for Django issue: ModelChoiceIteratorValue is not hashable.

This test confirms that ModelChoiceIteratorValue can be used in hash contexts
as dict keys and in sets, which is what was broken in Django 3.1.

Before the fix, trying to use ModelChoiceIteratorValue in these contexts
would raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
"""

from django.test import TestCase


class ModelChoiceIteratorValueTest(TestCase):
    def test_model_choice_iterator_value_is_hashable(self):
        """Test that ModelChoiceIteratorValue can be used as a dict key and in sets."""
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create test model-like objects
        class MockModel:
            def __init__(self, pk, name):
                self.pk = pk
                self.name = name
                
        instance = MockModel(1, 'test')
        
        # Create a ModelChoiceIteratorValue (this represents what's created internally by ModelChoiceField)
        value = ModelChoiceIteratorValue(1, instance)
        
        # Before the fix, the following operations would raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        # Test that it works as a dict key (this is the core functionality needed for the bug report)
        test_dict = {value: "test_value"}
        self.assertEqual(test_dict[value], "test_value")
        
        # Test that it works in sets (enables operations like value in some_set)
        test_set = {value}
        self.assertIn(value, test_set)
        
        # Test that it's actually hashable (the core change)
        hash_value = hash(value)
        self.assertIsInstance(hash_value, int)

    def test_model_choice_iterator_value_membership_operations(self):
        """Test that ModelChoiceIteratorValue works in membership operations."""
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create test model-like objects
        class MockModel:
            def __init__(self, pk, name):
                self.pk = pk
                self.name = name
                
        instance1 = MockModel(1, 'test1')
        instance2 = MockModel(2, 'test2')
        
        # Create ModelChoiceIteratorValues
        value1 = ModelChoiceIteratorValue(1, instance1)
        value2 = ModelChoiceIteratorValue(2, instance2)
        
        # Test that they work in sets for membership checking (like 'value in some_dict')
        test_set = {value1, value2}
        self.assertIn(value1, test_set)
        self.assertIn(value2, test_set)