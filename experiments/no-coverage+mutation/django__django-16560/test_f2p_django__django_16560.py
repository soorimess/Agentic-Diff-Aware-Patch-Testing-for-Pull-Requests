from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase


class TestBaseConstraintViolationErrorCode(TestCase):
    """Test that BaseConstraint can accept violation_error_code parameter."""
    
    def test_base_constraint_accepts_violation_error_code(self):
        """Test that BaseConstraint.__init__ accepts violation_error_code parameter."""
        # After the fix, this should work
        constraint = models.BaseConstraint(
            name="test_constraint",
            violation_error_code="custom_error_code",
            violation_error_message="Custom error message"
        )
        # Verify the code is stored correctly
        self.assertEqual(constraint.violation_error_code, "custom_error_code")


class TestCheckConstraintViolationErrorCode(TestCase):
    """Test that CheckConstraint can accept violation_error_code parameter."""
    
    def test_check_constraint_accepts_violation_error_code(self):
        """Test that CheckConstraint.__init__ accepts violation_error_code parameter."""
        # After the fix, this should work
        constraint = models.CheckConstraint(
            check=models.Q(price__gt=0),
            name="price_check",
            violation_error_code="price_invalid"
        )
        # Verify the code is stored correctly
        self.assertEqual(constraint.violation_error_code, "price_invalid")


class TestUniqueConstraintViolationErrorCode(TestCase):
    """Test that UniqueConstraint can accept violation_error_code parameter."""
    
    def test_unique_constraint_accepts_violation_error_code(self):
        """Test that UniqueConstraint.__init__ accepts violation_error_code parameter."""
        # After the fix, this should work
        constraint = models.UniqueConstraint(
            fields=["name"],
            name="unique_name",
            violation_error_code="name_duplicate"
        )
        # Verify the code is stored correctly
        self.assertEqual(constraint.violation_error_code, "name_duplicate")