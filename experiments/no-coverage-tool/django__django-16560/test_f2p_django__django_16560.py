from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint
from django.test import TestCase

from django.contrib.postgres.constraints import ExclusionConstraint


class ConstraintViolationErrorCodeTest(TestCase):
    def test_base_constraint_accepts_violation_error_code(self):
        """Test that BaseConstraint accepts violation_error_code parameter."""
        # Test that the violation_error_code parameter can be passed to CheckConstraint
        constraint = CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name="test_check_constraint",
            violation_error_code="my_custom_code"
        )
        
        # The violation_error_code should be stored
        self.assertEqual(constraint.violation_error_code, "my_custom_code")

    def test_unique_constraint_accepts_violation_error_code(self):
        """Test that UniqueConstraint accepts violation_error_code parameter."""
        # Test that the violation_error_code parameter can be passed to UniqueConstraint
        constraint = UniqueConstraint(
            fields=['name', 'color'],
            name="test_unique_constraint",
            violation_error_code="unique_constraint_violation"
        )
        
        # The violation_error_code should be stored
        self.assertEqual(constraint.violation_error_code, "unique_constraint_violation")

    def test_exclusion_constraint_accepts_violation_error_code(self):
        """Test that ExclusionConstraint accepts violation_error_code parameter."""
        # Test that the violation_error_code parameter can be passed to ExclusionConstraint
        constraint = ExclusionConstraint(
            expressions=[('name', '=')],
            name="test_exclusion_constraint",
            violation_error_code="exclusion_constraint_violation"
        )
        
        # The violation_error_code should be stored
        self.assertEqual(constraint.violation_error_code, "exclusion_constraint_violation")

    def test_constraint_repr_includes_violation_error_code(self):
        """Test that constraint repr includes violation_error_code when set."""
        constraint = CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name="test_check_constraint",
            violation_error_code="custom_check_code"
        )
        
        # The repr should include the violation error code
        repr_str = repr(constraint)
        self.assertIn("violation_error_code='custom_check_code'", repr_str)

    def test_constraint_equality_considers_violation_error_code(self):
        """Test that constraint equality considers violation_error_code."""
        constraint1 = CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name="test_check_constraint",
            violation_error_code="custom_code1"
        )
        
        constraint2 = CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name="test_check_constraint",
            violation_error_code="custom_code2"
        )
        
        constraint3 = CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name="test_check_constraint",
            violation_error_code="custom_code1"
        )
        
        # Constraints with different codes should not be equal
        self.assertNotEqual(constraint1, constraint2)
        # Constraints with same code should be equal
        self.assertEqual(constraint1, constraint3)
        
        # Test with UniqueConstraint too
        unique1 = UniqueConstraint(
            fields=['name', 'color'],
            name="test_unique_constraint",
            violation_error_code="unique_code1"
        )
        
        unique2 = UniqueConstraint(
            fields=['name', 'color'],
            name="test_unique_constraint",
            violation_error_code="unique_code2"
        )
        
        unique3 = UniqueConstraint(
            fields=['name', 'color'],
            name="test_unique_constraint",
            violation_error_code="unique_code1"
        )
        
        # Constraints with different codes should not be equal
        self.assertNotEqual(unique1, unique2)
        # Constraints with same code should be equal
        self.assertEqual(unique1, unique3)

    def test_constraint_deconstruct_includes_violation_error_code(self):
        """Test that constraint deconstruct includes violation_error_code when set."""
        constraint = CheckConstraint(
            check=models.Q(price__gt=models.F('discounted_price')),
            name="test_check_constraint", 
            violation_error_code="custom_deconstruct_code"
        )
        
        # Get the deconstructed representation
        path, args, kwargs = constraint.deconstruct()
        
        # Should include the violation_error_code
        self.assertIn('violation_error_code', kwargs)
        self.assertEqual(kwargs['violation_error_code'], "custom_deconstruct_code")
        
        # Test with UniqueConstraint too
        unique_constraint = UniqueConstraint(
            fields=['name', 'color'],
            name="test_unique_constraint",
            violation_error_code="unique_deconstruct_code"
        )
        
        path, args, kwargs = unique_constraint.deconstruct()
        self.assertIn('violation_error_code', kwargs)
        self.assertEqual(kwargs['violation_error_code'], "unique_deconstruct_code")