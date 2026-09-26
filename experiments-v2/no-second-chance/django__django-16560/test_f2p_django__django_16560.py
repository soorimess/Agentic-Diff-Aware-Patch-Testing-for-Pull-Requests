from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase


class TestConstraintErrorCode(TestCase):
    def test_constraint_error_code_functionality(self):
        """Test that all constraint types support violation_error_code parameter."""
        # Test BaseConstraint
        base_constraint = models.BaseConstraint(
            name="base_test",
            violation_error_code="base_error_code"
        )
        self.assertEqual(base_constraint.violation_error_code, "base_error_code")
        
        # Test CheckConstraint
        check_constraint = models.CheckConstraint(
            check=models.Q(price__gt=models.F("discounted_price")),
            name="check_test",
            violation_error_code="check_error_code"
        )
        self.assertEqual(check_constraint.violation_error_code, "check_error_code")
        
        # Test UniqueConstraint
        unique_constraint = models.UniqueConstraint(
            fields=["name"],
            name="unique_test",
            violation_error_code="unique_error_code"
        )
        self.assertEqual(unique_constraint.violation_error_code, "unique_error_code")

    def test_constraint_equality_with_error_codes(self):
        """Test that constraints with different error codes are not equal."""
        # CheckConstraint with different error codes
        constraint1 = models.CheckConstraint(
            check=models.Q(price__gt=models.F("discounted_price")),
            name="test",
            violation_error_code="error1"
        )
        constraint2 = models.CheckConstraint(
            check=models.Q(price__gt=models.F("discounted_price")),
            name="test",
            violation_error_code="error2"
        )
        self.assertNotEqual(constraint1, constraint2)
        
        # UniqueConstraint with different error codes
        unique1 = models.UniqueConstraint(
            fields=["name"],
            name="unique_test",
            violation_error_code="error1"
        )
        unique2 = models.UniqueConstraint(
            fields=["name"],
            name="unique_test",
            violation_error_code="error2"
        )
        self.assertNotEqual(unique1, unique2)

    def test_constraint_repr_includes_error_code(self):
        """Test that constraint repr includes error code when present."""
        constraint = models.CheckConstraint(
            check=models.Q(price__gt=models.F("discounted_price")),
            name="test",
            violation_error_code="custom_error"
        )
        repr_str = repr(constraint)
        self.assertIn("violation_error_code='custom_error'", repr_str)
        
        # Test with None error code
        constraint_no_code = models.CheckConstraint(
            check=models.Q(price__gt=models.F("discounted_price")),
            name="test"
        )
        repr_str = repr(constraint_no_code)
        self.assertNotIn("violation_error_code", repr_str)

    def test_constraint_default_behavior(self):
        """Test that constraints default to None error code when not specified."""
        # Test BaseConstraint default
        base_constraint = models.BaseConstraint(name="test")
        self.assertIsNone(base_constraint.violation_error_code)
        
        # Test CheckConstraint default
        check_constraint = models.CheckConstraint(
            check=models.Q(price__gt=models.F("discounted_price")),
            name="test"
        )
        self.assertIsNone(check_constraint.violation_error_code)
        
        # Test UniqueConstraint default
        unique_constraint = models.UniqueConstraint(
            fields=["name"],
            name="test"
        )
        self.assertIsNone(unique_constraint.violation_error_code)

    def test_constraint_deconstruct_includes_error_code(self):
        """Test that deconstruct method includes violation_error_code when set."""
        constraint = models.BaseConstraint(
            name="test",
            violation_error_code="test_error"
        )
        path, args, kwargs = constraint.deconstruct()
        self.assertIn("violation_error_code", kwargs)
        self.assertEqual(kwargs["violation_error_code"], "test_error")
        
        # Test default case
        constraint_default = models.BaseConstraint(name="test")
        path, args, kwargs = constraint_default.deconstruct()
        self.assertNotIn("violation_error_code", kwargs)