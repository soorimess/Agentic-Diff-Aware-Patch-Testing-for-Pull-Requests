"""
Regression test for Django issue #14915: ModelChoiceIteratorValue is not hashable.
"""
from django.test import TestCase
from django.forms.models import ModelChoiceIteratorValue


class ModelChoiceIteratorValueHashTest(TestCase):
    def test_model_choice_iterator_value_is_hashable(self):
        """
        Test that ModelChoiceIteratorValue can be used as a dictionary key.
        
        Before fix: TypeError: unhashable type: 'ModelChoiceIteratorValue' 
        After fix: Should work without error
        """
        # Create a ModelChoiceIteratorValue instance
        value = ModelChoiceIteratorValue("test_value", "test_instance")
        
        # Try using it as a dict key - should not raise TypeError
        try:
            test_dict = {value: "test_data"}
            result = test_dict[value]
            # Should be able to retrieve the value
            self.assertEqual(result, "test_data")
        except TypeError as e:
            if "unhashable type" in str(e) and "ModelChoiceIteratorValue" in str(e):
                self.fail("ModelChoiceIteratorValue is not hashable: %s" % str(e))
            else:
                raise  # Re-raise if it's a different error

    def test_model_choice_iterator_value_hash_consistency(self):
        """
        Test that equal ModelChoiceIteratorValue instances have consistent hash values.
        """
        value1 = ModelChoiceIteratorValue("test", "obj1")
        value2 = ModelChoiceIteratorValue("test", "obj2")  # Same value, different instance
        
        # Both should be hashable 
        try:
            hash1 = hash(value1)
            hash2 = hash(value2)
            # They should be equal since they are equal and have same value
            self.assertEqual(hash1, hash2)
        except TypeError as e:
            if "unhashable type" in str(e) and "ModelChoiceIteratorValue" in str(e):
                self.fail("ModelChoiceIteratorValue is not hashable for consistency test: %s" % str(e))
            else:
                raise