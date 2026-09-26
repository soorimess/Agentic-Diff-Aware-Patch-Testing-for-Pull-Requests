import unittest

from django.forms.models import ModelChoiceIteratorValue


class TestModelChoiceIteratorValueHashable(unittest.TestCase):
    def test_model_choice_iterator_value_is_hashable(self):
        """Test that ModelChoiceIteratorValue is hashable to prevent TypeError."""
        # Create a ModelChoiceIteratorValue directly with a simple value
        value = ModelChoiceIteratorValue("test_value", "test_instance")
        
        # This should not raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        try:
            hash_value = hash(value)
            # If we get here without exception, the value is hashable
            self.assertIsNotNone(hash_value)
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue is not hashable: {e}")

    def test_model_choice_iterator_value_in_dict_membership(self):
        """Test that ModelChoiceIteratorValue can be used as dict key."""
        # Create a ModelChoiceIteratorValue directly
        value = ModelChoiceIteratorValue("test_value", "test_instance")
        
        # This should work without TypeError
        # The bug report shows this pattern: value in self.show_fields where show_fields is a dict
        show_fields = {"test_value": ['first_name', 'last_name']}
        
        try:
            # This line would fail before the fix with "TypeError: unhashable type: 'ModelChoiceIteratorValue'"
            if value in show_fields:
                pass
            self.assertTrue(True)
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue cannot be used in dict membership test: {e}")

    def test_model_choice_iterator_value_in_set_membership(self):
        """Test that ModelChoiceIteratorValue can be used in set membership."""
        # Create a ModelChoiceIteratorValue directly
        value = ModelChoiceIteratorValue("test_value", "test_instance")
        
        # This should work without TypeError
        allowed_values = ["test_value", "other_value"]
        
        try:
            # This line would fail before the fix with "TypeError: unhashable type: 'ModelChoiceIteratorValue'"
            if value in allowed_values:
                pass
            self.assertTrue(True)
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue cannot be used in set membership test: {e}")

    def test_model_choice_iterator_value_hash_based_on_value(self):
        """Test that ModelChoiceIteratorValue hash is based on its value, not arbitrary."""
        # Create two ModelChoiceIteratorValue instances with same value
        value1 = ModelChoiceIteratorValue("test_value", "test_instance1")
        value2 = ModelChoiceIteratorValue("test_value", "test_instance2")
        
        # They should have the same hash since they have the same value
        self.assertEqual(hash(value1), hash(value2))
        
        # Create one with different value
        value3 = ModelChoiceIteratorValue("different_value", "test_instance3")
        
        # They should have different hashes
        self.assertNotEqual(hash(value1), hash(value3))