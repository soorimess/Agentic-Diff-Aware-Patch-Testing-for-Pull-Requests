from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint
from django.contrib.postgres.constraints import ExclusionConstraint
from django.test import TestCase


class TestConstraintViolationErrorCode(TestCase):
    def test_check_constraint_accepts_violation_error_code_parameter(self):
        """Test that CheckConstraint accepts violation_error_code parameter."""
        # This should work after the fix - test that the parameter can be passed
        constraint = CheckConstraint(
            check=models.Q(name__startswith="A"),
            name="test_check_constraint",
            violation_error_code="custom_code"
        )
        # If we get here without TypeError, the parameter is accepted
        self.assertEqual(constraint.violation_error_code, "custom_code")

    def test_unique_constraint_accepts_violation_error_code_parameter(self):
        """Test that UniqueConstraint accepts violation_error_code parameter."""
        # This should work after the fix - test that the parameter can be passed
        constraint = UniqueConstraint(
            fields=['name'],
            name="test_unique_constraint",
            violation_error_code="unique_code"
        )
        # If we get here without TypeError, the parameter is accepted
        self.assertEqual(constraint.violation_error_code, "unique_code")

    def test_exclusion_constraint_accepts_violation_error_code_parameter(self):
        """Test that ExclusionConstraint accepts violation_error_code parameter."""
        # This should work after the fix - test that the parameter can be passed
        constraint = ExclusionConstraint(
            expressions=[('name', '==')],
            name="test_exclusion_constraint",
            violation_error_code="exclusion_code"
        )
        # If we get here without TypeError, the parameter is accepted
        self.assertEqual(constraint.violation_error_code, "exclusion_code")