"""
Regression test for Django issue where ModelChoiceIteratorValue is not hashable.
This test should fail on the old code (missing __hash__ method) and pass after the fix.
"""
import sys
import os

# Add current directory to Python path so we can import Django
sys.path.insert(0, '/testbed')

# Import django before creating the test to avoid init issues
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.test_sqlite')
import django
django.setup()

from django.test import TestCase


class ModelChoiceIteratorValueTests(TestCase):
    
    def test_model_choice_iterator_value_hashable(self):
        """Test that ModelChoiceIteratorValue instances are hashable."""
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create a simple ModelChoiceIteratorValue instance 
        value = ModelChoiceIteratorValue("test_value", "test_instance")
        
        # This should work after the fix, but fail before (TypeError: unhashable type)
        try:
            hash_value = hash(value)
            # If we get here without exception, the hash worked  
            self.assertIsInstance(hash_value, int)
        except TypeError as e:
            # This should not happen after the fix but will happen before
            if "unhashable type" in str(e) and "ModelChoiceIteratorValue" in str(e):
                self.fail("ModelChoiceIteratorValue is not hashable")
            raise e
    
    def test_model_choice_iterator_value_in_dict(self):
        """Test that ModelChoiceIteratorValue can be used as dict key."""
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create ModelChoiceIteratorValue instances
        value1 = ModelChoiceIteratorValue("value1", "instance1") 
        value2 = ModelChoiceIteratorValue("value2", "instance2")
        
        # Create a dict with ModelChoiceIteratorValue keys
        test_dict = {value1: "associated_data1", value2: "associated_data2"}
        
        # This should work after fix, would raise TypeError before
        self.assertEqual(test_dict[value1], "associated_data1")
        self.assertEqual(test_dict[value2], "associated_data2")
        
        # Test membership testing that would be in dictionary lookups like in bug report
        test_dict = {"key1": "data1", "key2": "data2"}
        # This is the case from bug report: value in self.show_fields where 
        # self.show_fields is a dict and value is a ModelChoiceIteratorValue
        try:
            # This should work if value is hashable
            result = value1 in test_dict
            # We don't care about result, just that it doesn't raise TypeError
        except TypeError as e:
            if "unhashable type" in str(e):
                self.fail("ModelChoiceIteratorValue cannot be used in membership test")
            raise e
    
    def test_model_choice_iterator_value_in_set(self):
        """Test that ModelChoiceIteratorValue can be used in sets."""
        from django.forms.models import ModelChoiceIteratorValue
        
        # Create ModelChoiceIteratorValue instances
        value1 = ModelChoiceIteratorValue("value1", "instance1")
        value2 = ModelChoiceIteratorValue("value2", "instance2")
        
        # This should work after the fix, fail before with TypeError
        try:
            test_set = {value1, value2}
            # If we get here, set creation worked
            self.assertEqual(len(test_set), 2) 
        except TypeError as e:
            if "unhashable type" in str(e):
                self.fail("ModelChoiceIteratorValue cannot be used in sets")
            raise e