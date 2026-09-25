"""
Regression test verifying that violation_error_code parameter is accepted in constraints.
This test should fail before the fix and pass after.
"""
from django.db import models
from django.test import SimpleTestCase


class TestConstraintCodeParameter(SimpleTestCase):
    def test_base_constraint_violation_error_code_parameter(self):
        """Test that BaseConstraint accepts violation_error_code."""
        # This should pass when the fix is applied
        # Before fix it will give TypeError about unexpected keyword argument
        constraint = models.BaseConstraint(
            name="test",
            violation_error_code="custom_error_code"
        )
        # After fix, this value should be stored
        self.assertEqual(constraint.violation_error_code, "custom_error_code")