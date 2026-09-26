import unittest

from django.forms.models import ModelChoiceIteratorValue


class TestModelChoiceIteratorValueHashable(unittest.TestCase):
    """Test that ModelChoiceIteratorValue is hashable."""

    def test_model_choice_iterator_value_is_hashable(self):
        """Test that ModelChoiceIteratorValue instances can be hashed."""
        # Create a ModelChoiceIteratorValue instance with simple values
        value = ModelChoiceIteratorValue(1, "test_instance")
        
        # This should not raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        try:
            hash(value)
            # If we get here, hashing worked
            self.assertTrue(True)
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue is not hashable: {e}")

    def test_model_choice_iterator_value_in_dict_membership(self):
        """Test that ModelChoiceIteratorValue can be used as dict key."""
        # Create a ModelChoiceIteratorValue instance
        value = ModelChoiceIteratorValue(1, "test_instance")
        
        # This should work without TypeError - simulating the bug report scenario
        # where value in self.show_fields would fail
        test_dict = {value: 'test_value'}
        self.assertEqual(test_dict[value], 'test_value')
        
        # Also test membership - this is what fails in the bug report
        self.assertIn(value, test_dict)

    def test_model_choice_iterator_value_in_set_membership(self):
        """Test that ModelChoiceIteratorValue can be used in sets."""
        # Create ModelChoiceIteratorValue instances
        value1 = ModelChoiceIteratorValue(1, "test_instance1")
        value2 = ModelChoiceIteratorValue(1, "test_instance2")  # Same value, different instance
        
        # This should work without TypeError
        test_set = {value1, value2}
        self.assertEqual(len(test_set), 2)  # Should contain both values
        
        # Test membership
        self.assertIn(value1, test_set)
        self.assertIn(value2, test_set)
        
    def test_model_choice_iterator_value_membership_scenario_from_bug_report(self):
        """
        Test the exact scenario from the bug report:
        Using value in self.show_fields where self.show_fields is a dict
        and value is a ModelChoiceIteratorValue.
        """
        # Create a ModelChoiceIteratorValue instance (simulating what comes from widget)
        value = ModelChoiceIteratorValue(1, "test_instance")
        
        # This simulates the bug report scenario: value in self.show_fields
        # where self.show_fields is a dict like {1: ['first_name', 'last_name']}
        show_fields = {1: ['first_name', 'last_name']}
        
        # Before the fix, this would raise TypeError: unhashable type: 'ModelChoiceIteratorValue'
        # After the fix, this should work correctly
        try:
            result = value in show_fields
            # If we get here without exception, the behavior is correct
            self.assertFalse(result)  # value (1) is not in show_fields keys as a ModelChoiceIteratorValue
        except TypeError as e:
            self.fail(f"ModelChoiceIteratorValue membership test failed: {e}")