"""
Regression test for Django issue where ModelChoiceIteratorValue is not hashable.

This test catches the specific bug mentioned in the issue where ModelChoiceIteratorValue
objects are not hashable, causing TypeError: unhashable type: 'ModelChoiceIteratorValue'
when used in operations like 'value in dict' or as set elements.

The bug was fixed by adding a __hash__ method to the ModelChoiceIteratorValue class.
"""
from django.test import TestCase
from django.forms.models import ModelChoiceIteratorValue


class ModelChoiceIteratorValueHashableTest(TestCase):
    def test_model_choice_iterator_value_can_be_used_in_dict_membership(self):
        """
        Test that ModelChoiceIteratorValue can be used in 'in' operations with dicts.
        This was failing with TypeError: unhashable type: 'ModelChoiceIteratorValue'
        before the fix was applied.
        """
        # Create a ModelChoiceIteratorValue like Django forms would
        value = ModelChoiceIteratorValue(1, 'test_instance')
        
        # This dict mimics the pattern from the bug report
        show_fields = {1: ['first_name', 'last_name']}
        
        # Before the fix, this would raise:
        # TypeError: unhashable type: 'ModelChoiceIteratorValue' 
        try:
            # This operation requires hashability
            if value in show_fields:
                pass
            # If we get here, it worked
        except TypeError as e:
            if 'unhashable type: \'ModelChoiceIteratorValue\'' in str(e):
                self.fail("ModelChoiceIteratorValue should be hashable for dict membership tests")
            raise

    def test_model_choice_iterator_value_is_hashable(self):
        """
        Test that ModelChoiceIteratorValue objects can be hashed.
        This ensures they can be used in sets and as dict keys.
        """
        # Create a ModelChoiceIteratorValue instance
        value = ModelChoiceIteratorValue('test_value', 'test_instance')
        
        # This should not raise TypeError about unhashable type
        try:
            # Test that hash() works
            hash_value = hash(value)
            
            # Test that it can be used in a set (which requires hashing)
            test_set = {value}
            
            # Test that it can be used as a dict key (which requires hashing)
            test_dict = {value: 'some_value'}
            
            # All operations succeeded - the test passes
        except TypeError as e:
            if 'unhashable type: \'ModelChoiceIteratorValue\'' in str(e):
                self.fail("ModelChoiceIteratorValue should be hashable but is not")
            raise