from django.db import models
from django.test import TestCase


class TestConstraintErrorCode(TestCase):
    def test_base_constraint_accepts_violation_error_code(self):
        """Test that BaseConstraint accepts violation_error_code parameter."""
        constraint = models.BaseConstraint(
            name="test_constraint",
            violation_error_code="custom_error_code",
            violation_error_message="Custom error message"
        )
        # Verify the code is stored
        self.assertEqual(constraint.violation_error_code, "custom_error_code")

    def test_check_constraint_accepts_violation_error_code(self):
        """Test that CheckConstraint accepts violation_error_code parameter."""
        constraint = models.CheckConstraint(
            check=models.Q(name__isnull=False),
            name="test_check_constraint",
            violation_error_code="check_error_code",
            violation_error_message="Check constraint failed"
        )
        # Verify the code is stored
        self.assertEqual(constraint.violation_error_code, "check_error_code")

    def test_unique_constraint_accepts_violation_error_code(self):
        """Test that UniqueConstraint accepts violation_error_code parameter."""
        constraint = models.UniqueConstraint(
            fields=["name"],
            name="test_unique_constraint",
            violation_error_code="unique_error_code",
            violation_error_message="Unique constraint failed"
        )
        # Verify the code is stored
        self.assertEqual(constraint.violation_error_code, "unique_error_code")