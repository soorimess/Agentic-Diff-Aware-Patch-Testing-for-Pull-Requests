from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase


class TestConstraintErrorCode(TestCase):
    def test_check_constraint_accepts_violation_error_code(self):
        """Test that CheckConstraint accepts violation_error_code parameter."""
        # This should work after the fix is applied
        constraint = models.CheckConstraint(
            check=models.Q(price__gt=models.F("discounted_price")),
            name="test_constraint",
            violation_error_code="custom_code"
        )
        
        # Verify the parameter is stored correctly
        self.assertEqual(constraint.violation_error_code, "custom_code")
        
        # Test that it also works with violation_error_message
        constraint2 = models.CheckConstraint(
            check=models.Q(price__gt=models.F("discounted_price")),
            name="test_constraint2",
            violation_error_code="custom_code",
            violation_error_message="Custom error message"
        )
        self.assertEqual(constraint2.violation_error_code, "custom_code")
        self.assertEqual(constraint2.violation_error_message, "Custom error message")

    def test_unique_constraint_accepts_violation_error_code(self):
        """Test that UniqueConstraint accepts violation_error_code parameter."""
        # This should work after the fix is applied
        constraint = models.UniqueConstraint(
            fields=["name"],
            name="test_constraint",
            violation_error_code="custom_code"
        )
        
        # Verify the parameter is stored correctly
        self.assertEqual(constraint.violation_error_code, "custom_code")
        
        # Test that it also works with violation_error_message
        constraint2 = models.UniqueConstraint(
            fields=["name"],
            name="test_constraint2",
            violation_error_code="custom_code",
            violation_error_message="Custom error message"
        )
        self.assertEqual(constraint2.violation_error_code, "custom_code")
        self.assertEqual(constraint2.violation_error_message, "Custom error message")

    def test_exclusion_constraint_accepts_violation_error_code(self):
        """Test that ExclusionConstraint accepts violation_error_code parameter."""
        try:
            from django.contrib.postgres.constraints import ExclusionConstraint
            
            # This should work after the fix is applied
            constraint = ExclusionConstraint(
                name="test_constraint",
                expressions=[("number", "=")],
                violation_error_code="custom_code"
            )
            
            # Verify the parameter is stored correctly
            self.assertEqual(constraint.violation_error_code, "custom_code")
            
            # Test that it also works with violation_error_message
            constraint2 = ExclusionConstraint(
                name="test_constraint2",
                expressions=[("number", "=")],
                violation_error_code="custom_code",
                violation_error_message="Custom error message"
            )
            self.assertEqual(constraint2.violation_error_code, "custom_code")
            self.assertEqual(constraint2.violation_error_message, "Custom error message")
        except ImportError:
            # Skip test if postgres is not available
            pass

    def test_constraint_deconstruct_includes_error_code(self):
        """Test that constraint deconstruct method includes violation_error_code."""
        # Test CheckConstraint
        constraint = models.CheckConstraint(
            check=models.Q(price__gt=models.F("discounted_price")),
            name="test_constraint",
            violation_error_code="custom_code"
        )
        
        # Check that deconstruct includes the violation_error_code
        path, args, kwargs = constraint.deconstruct()
        self.assertIn('violation_error_code', kwargs)
        self.assertEqual(kwargs['violation_error_code'], "custom_code")
        
        # Test UniqueConstraint
        constraint2 = models.UniqueConstraint(
            fields=["name"],
            name="test_constraint2",
            violation_error_code="custom_code"
        )
        
        # Check that deconstruct includes the violation_error_code
        path2, args2, kwargs2 = constraint2.deconstruct()
        self.assertIn('violation_error_code', kwargs2)
        self.assertEqual(kwargs2['violation_error_code'], "custom_code")