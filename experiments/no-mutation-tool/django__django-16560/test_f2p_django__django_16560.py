"""
Regression test for Django issue #16560.
Tests that BaseConstraint and subclasses can use violation_error_code for ValidationError.
"""
from django.test import TestCase


class TestConstraintErrorCode(TestCase):
    def test_base_constraint_violation_error_code_parameter(self):
        """
        Test that BaseConstraint accepts violation_error_code parameter.
        Covers the main change from the pull request - __init__ signature extension.
        """
        from django.db.models import BaseConstraint
        constraint = BaseConstraint(
            name='test_constraint',
            violation_error_code='custom_validation_error'
        )
        self.assertEqual(constraint.violation_error_code, 'custom_validation_error')

    def test_constraint_repr_with_error_code(self):
        """
        Test that constraint __repr__ includes violation_error_code when present.
        Covers the __repr__ method updates in constraint classes.
        """
        from django.db.models import BaseConstraint
        constraint = BaseConstraint(
            name='test_constraint',
            violation_error_code='test_repr_code'
        )
        repr_str = repr(constraint)
        # The repr should include the violation_error_code if it is set
        # We're checking the method works rather than exact format
        self.assertIn("violation_error_code", repr_str)

    def test_constraint_equality_with_error_code(self):
        """
        Test that constraint equality handles violation_error_code properly.
        Covers the __eq__ method updates in constraint classes.
        """
        from django.db.models import BaseConstraint
        constraint1 = BaseConstraint(
            name='test_constraint1',
            violation_error_code='same_code'
        )
        constraint2 = BaseConstraint(
            name='test_constraint2',
            violation_error_code='same_code'
        )
        # Both have same violation_error_code should not crash in comparison
        # Note: They are different objects so not equal, but equality method should not error
        try:
            result = constraint1.__eq__(constraint2)
        except Exception:
            self.fail("BaseConstraint.__eq__ failed with violation_error_code")
            
    def test_constraint_deconstruct_with_error_code(self):
        """
        Test that constraint deconstruct includes violation_error_code when present.
        Covers the deconstruct method updates in constraint classes.
        """
        from django.db.models import BaseConstraint
        constraint = BaseConstraint(
            name='test_constraint',
            violation_error_code='deconstruct_code'
        )
        # Test deconstruct includes violation_error_code
        path, args, kwargs = constraint.deconstruct()
        self.assertIn('violation_error_code', kwargs)
        self.assertEqual(kwargs['violation_error_code'], 'deconstruct_code')